#把MNIST像素从0-255缩放到0.01-1.0

def scale_inputs(pixel_values):

    inputs = []

    for pixel in pixel_values:
        pixel = int(pixel)

        if pixel < 0:
            pixel = 0

        if pixel > 255:
            pixel = 255

        scaled_value = pixel / 255.0 * 0.99 + 0.01
        inputs.append(scaled_value)

    return inputs

# 根据label创建目标输出，如果label=7，第7个位置是 0.99,其余位置是0.01
def create_targets(label, output_nodes=10):

    targets = []

    for i in range(output_nodes):
        targets.append(0.01)

    targets[int(label)] = 0.99

    return targets

#从一行MNIST_CSV数据里取出label
def get_label(record):

    all_values = record.strip().split(',')
    label = int(all_values[0])

    return label

    
#从一行MNIST_CSV数据里取出784个像素,并缩放
def get_inputs(record):

    all_values = record.strip().split(',')
    pixel_values = all_values[1:]

    inputs = scale_inputs(pixel_values)

    return inputs

    
#从一行MNIST CSV数据里取出label,并生成targets
def get_targets(record, output_nodes=10):

    label = get_label(record)
    targets = create_targets(label, output_nodes)

    return targets

#找出列表中最大值的位置,用来判断神经网络预测的是哪个数字
def get_max_index(values):

    max_value = values[0]
    max_index = 0

    for i in range(1, len(values)):
        if values[i] > max_value:
            max_value = values[i]
            max_index = i

    return max_index