import math
import random


class NeuralNetwork:
    def __init__(self, input_nodes, hidden_nodes, output_nodes, learning_rate):
        #初始化神经网络

        #input_nodes: 输入层节点数量
        #hidden_nodes: 隐藏层节点数量
        #output_nodes: 输出层节点数量
        #learning_rate: 学习率

        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes
        self.learning_rate = learning_rate

        # wih = input layer 到 hidden layer 的权重矩阵
        # 行数 = hidden_nodes
        # 列数 = input_nodes
        self.wih = self.create_weights(self.hidden_nodes, self.input_nodes)

        # who = hidden layer 到 output layer 的权重矩阵
        # 行数 = output_nodes
        # 列数 = hidden_nodes
        self.who = self.create_weights(self.output_nodes, self.hidden_nodes)

    def create_weights(self, rows, cols):
        
        #创建随机权重matrix

        weights = []

        standard_deviation = pow(cols, -0.5)

        for r in range(rows):
            row = []

            for c in range(cols):
                value = random.gauss(0.0, standard_deviation)
                row.append(value)

            weights.append(row)

        return weights

    def sigmoid(self, x):
        
        #sigmoid函数

        #sigmoid(x) = 1 / (1 + e^(-x))

        return 1 / (1 + math.exp(-x))

    def matrix_vector_dot(self, matrix, vector):
        
        #matrix的×向量
        #把上一层所有节点的输出，通过权重矩阵，计算出下一层每个节点的加权输入

        result = []

        for row in matrix:
            total = 0

            for i in range(len(vector)):
                total += row[i] * vector[i]

            result.append(total)

        return result

    def apply_sigmoid(self, values):
        #对列表中的每个值都使用sigmoid
        

        result = []

        for value in values:
            result.append(self.sigmoid(value))

        return result

    def vector_subtract(self, a, b):
        
        #向量相减,计算errors=targets-outputs

        result = []

        for i in range(len(a)):
            result.append(a[i] - b[i])

        return result

    def transpose(self, matrix):
        #inverse matrix
        #反向传播时需要用who的transpose：
        #hidden_errors=transpose(who)×output_errors


        result = []

        for col in range(len(matrix[0])):
            new_row = []

            for row in range(len(matrix)):
                new_row.append(matrix[row][col])

            result.append(new_row)

        return result

    def query(self, inputs):
        #查询神经网络
        #也就是前向传播：
        #inputs->hidden layer->output layer

        # input layer->hidden layer
        hidden_inputs = self.matrix_vector_dot(self.wih, inputs)
        hidden_outputs = self.apply_sigmoid(hidden_inputs)

        # hidden layer->output layer
        final_inputs = self.matrix_vector_dot(self.who, hidden_outputs)
        final_outputs = self.apply_sigmoid(final_inputs)

        return final_outputs

    def train(self, inputs, targets):
        #训练神经网络。

        #完整流程：
        #1. 前向传播，得到outputs
        #2. 计算output_errors
        #3. 反向传播，得到hidden_errors
        #4. 更新who
        #5. 更新wih

        # 1.向前传播

        # input layer->hidden layer
        hidden_inputs = self.matrix_vector_dot(self.wih, inputs)
        hidden_outputs = self.apply_sigmoid(hidden_inputs)

        # hidden layer->output layer
        final_inputs = self.matrix_vector_dot(self.who, hidden_outputs)
        final_outputs = self.apply_sigmoid(final_inputs)

        # 2. 计算输出层误差

        # output_errors=targets-final_outputs
        output_errors = self.vector_subtract(targets, final_outputs)

        # 3. 反向传播误差到隐藏层

        # 这里要先用旧的who计算hidden_errors
        who_transposed = self.transpose(self.who)
        hidden_errors = self.matrix_vector_dot(who_transposed, output_errors)

        # 更新 hidden->output的权重who

        for output_index in range(self.output_nodes):
            for hidden_index in range(self.hidden_nodes):

                #权重变化量=learning_rate×output_error×final_output×(1-final_output)×hidden_output

                change = (
                    self.learning_rate
                    * output_errors[output_index]
                    * final_outputs[output_index]
                    * (1 - final_outputs[output_index])
                    * hidden_outputs[hidden_index]
                )

                self.who[output_index][hidden_index] += change

        # 5. 更新input->hidden的权重wih

        for hidden_index in range(self.hidden_nodes):
            for input_index in range(self.input_nodes):

                #权重变化量=learning_rate×hidden_error×hidden_output×(1-hidden_output)×input

                change = (
                    self.learning_rate
                    * hidden_errors[hidden_index]
                    * hidden_outputs[hidden_index]
                    * (1 - hidden_outputs[hidden_index])
                    * inputs[input_index]
                )

                self.wih[hidden_index][input_index] += change