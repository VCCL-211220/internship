from neural_network import NeuralNetwork
from tools import get_inputs, get_targets, get_label, get_max_index


#设置参数

input_nodes = 784
hidden_nodes = 100
output_nodes = 10
learning_rate = 0.3

network = NeuralNetwork(
    input_nodes,
    hidden_nodes,
    output_nodes,
    learning_rate
)


#读取训练样本和测试样本

training_data_file = open("neural_network/mnist/mnist_train_100.csv", "r")
training_data_list = training_data_file.readlines()
training_data_file.close()


#训练神经网络

epochs = 5

max_train_records = 100

for epoch in range(epochs):

    count = 0

    for record in training_data_list:
        if record.strip() == "":
            continue

        inputs = get_inputs(record)
        targets = get_targets(record, output_nodes)

        network.train(inputs, targets)

        count += 1

        if count >= max_train_records:
            break
print("训练第", epoch + 1, "轮")
print("训练完成")


#读取测试数据

test_data_file = open("neural_network/mnist/mnist_test_10.csv", "r")
test_data_list = test_data_file.readlines()
test_data_file.close()


#检查神经网络答案

scorecard = []

max_test_records = 10

count = 0

for record in test_data_list:
    if record.strip() == "":
        continue

    correct_label = get_label(record)

    inputs = get_inputs(record)

    outputs = network.query(inputs)

    label = get_max_index(outputs)

    if label == correct_label:
        scorecard.append(1)
    else:
        scorecard.append(0)

    count += 1

    if count >= max_test_records:
        break


#计算准确率

correct_count = 0

for score in scorecard:
    correct_count += score

performance = correct_count / len(scorecard)

print("正确数量:", correct_count)
print("测试总数:", len(scorecard))
print("准确率:", performance)