from flask import Flask, request, jsonify
from flask_cors import CORS
import os

from neural_network import NeuralNetwork
from tools import get_inputs, get_targets, get_max_index, scale_inputs


app = Flask(__name__)
CORS(app)

app.json.ensure_ascii = False


# 保存训练好的神经网络模型
network = None


def train_model():
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

    base_dir = os.path.dirname(os.path.abspath(__file__))
    train_path = os.path.join(base_dir, "mnist", "mnist_train_100.csv")

    training_data_file = open(train_path, "r")
    training_data_list = training_data_file.readlines()
    training_data_file.close()

    epochs = 1
    max_train_records = 10

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


@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "success": True,
        "message": "backend is running"
    })


@app.route("/api/predict", methods=["POST"])
def predict_digit():
    try:
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

    except Exception as error:
        print("Predict error:", error)

        return jsonify({
            "success": False,
            "message": str(error)
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
