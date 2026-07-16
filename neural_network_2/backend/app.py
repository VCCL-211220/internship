from flask import Flask, request, jsonify
from flask_cors import CORS

from neural_network import NeuralNetwork
from tools import get_inputs, get_targets, get_max_index, scale_inputs


app = Flask(__name__)
CORS(app)

app.json.ensure_ascii = False


# 保存训练好的神经网络模型
network = None


def train_model():
    # 设置神经网络参数
    input_nodes = 784
    hidden_nodes = 100
    output_nodes = 10
    learning_rate = 0.3

    model = NeuralNetwork(
        input_nodes,
        hidden_nodes,
        output_nodes,
        learning_rate
    )

    # 读取 MNIST 训练数据
    training_data_file = open("mnist/mnist_train_100.csv", "r")
    training_data_list = training_data_file.readlines()
    training_data_file.close()

    # 训练模型
    epochs = 5
    max_train_records = 100

    for epoch in range(epochs):
        count = 0

        for record in training_data_list:
            if record.strip() == "":
                continue

            inputs = get_inputs(record)
            targets = get_targets(record, output_nodes)

            model.train(inputs, targets)

            count += 1

            if count >= max_train_records:
                break

    return model


def get_model():
    global network

    if network is None:
        network = train_model()

    return network


@app.route("/api/predict", methods=["POST"])
def predict_digit():
    data = request.get_json()

    if data is None:
        return jsonify({
            "success": False,
            "message": "没有收到 JSON 数据"
        }), 400

    pixels = data.get("pixels")

    if pixels is None:
        return jsonify({
            "success": False,
            "message": "缺少 pixels 数据"
        }), 400

    if len(pixels) != 784:
        return jsonify({
            "success": False,
            "message": "pixels 长度必须是 784"
        }), 400

    model = get_model()

    inputs = scale_inputs(pixels)

    outputs = model.query(inputs)

    label = get_max_index(outputs)

    scores = []

    for value in outputs:
        scores.append(round(value, 4))

    return jsonify({
        "success": True,
        "label": label,
        "scores": scores
    })


if __name__ == "__main__":
    app.run(debug=True)