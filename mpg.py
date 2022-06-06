import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns  # 使用 seaborn 绘制矩阵图 (pairplot)
import tensorflow as tf
import tensorflow.keras as keras
import tensorflow.keras.layers as layers

"""
利用全连接网络模型来完成汽车的效能指标 MPG(Mile Per Gallon，每加仑燃油英里数)的预测问题实战。
Auto MPG 数据集一共记录了 398 项数据
"""

# 在线下载汽车效能数据集
dataset_path = keras.utils.get_file("auto-mpg.data",
                                    "http://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data")

# 利用 pandas 读取数据集，字段有效能（公里数每加仑），气缸数，排量，马力，重量加速度，型号年份，产地
column_names = ['MPG', 'Cylinders', 'Displacement', 'Horsepower', 'Weight',
                'Acceleration', 'Model Year', 'Origin']

"""
sep: 指定分割符，默认是’,’C引擎不能自动检测分隔符，但Python解析引擎可以
names: 指定列名，如果文件中不包含header的行，应该显性表示header=None
na_values: 默认None NaN包含哪些情况，默认情况下, ‘#N/A’, ‘#N/A N/A’, ‘#NA’, ‘-1.#IND’, ‘-1.#QNAN’, ‘-NaN’, ‘-nan’, ‘1.#IND’, ‘1.#QNAN’, ‘N/A’, ‘NA’, ‘NULL’, ‘NaN’, ‘n/a’, ‘nan’, ‘null’. 都表现为NAN
skipinitialspace: 忽略分隔符后的空格,默认false
标识着多余的行不被解析。如果该字符出现在行首，这一行将被全部忽略。这个参数只能是一个字符，空行（就像skip_blank_lines=True）注释行被header和skiprows忽略一样。例如如果指定comment='#' 解析‘#empty\na,b,c\n1,2,3’ 以header=0 那么返回结果将是以’a,b,c'作为header。
"""
raw_dataset = pd.read_csv(dataset_path, names=column_names,
                          na_values="?", comment='\t',
                          sep=" ", skipinitialspace=True)
dataset = raw_dataset.copy()
# 查看部分数据
print(dataset.head())

# 原始表格中的数据可能含有空字段(缺失值)的数据项，需要清除这些记录项：
print("删除空白数据项前：\n{sum}\n".format(sum=dataset.isna().sum()))  # 统计空白数据
dataset = dataset.dropna()  # 删除空白数据项
print("删除空白数据项后：\n{sum}\n".format(sum=dataset.isna().sum()))  # 再次统计空白数据

"""
清除后，观察到数据集记录项减为392项。
由于Origin字段为类别类型数据，我们将其移除，并转换为新的3个字段：USA、Europe和Japan，分别代表是否来自此产地：
"""
# 处理类别型数据，其中 origin 列代表了类别 1,2,3,分布代表产地：美国、欧洲、日本
# 先弹出(删除并返回)origin 这一列
origin = dataset.pop('Origin')
# 根据 origin 列来写入新的 3 个列
dataset['USA'] = (origin == 1) * 1.0
dataset['Europe'] = (origin == 2) * 1.0
dataset['Japan'] = (origin == 3) * 1.0
# 查看新表格的后几项
print("查看新表格的后几项：\n{tail}\n".format(tail=dataset.tail()))

# 按着8: 2的比例切分数据集为训练集和测试集：
# 切分为训练集和测试集
train_dataset = dataset.sample(frac=0.8, random_state=0)
test_dataset = dataset.drop(train_dataset.index)

# 数据检查: 快速查看训练集中几对列的联合分布
sns.pairplot(train_dataset[["MPG", "Cylinders", "Displacement", "Weight"]], diag_kind="kde")

"""
统计训练集的各个字段数值的均值和标准差，并完成数据的标准化，通过norm()函数实现
"""
# 查看训练集的输入 X 的统计数据
train_stats = train_dataset.describe()
print("train_stats：\n{train_stats}\n".format(train_stats=train_stats))
train_stats.pop("MPG")  # 仅保留输入 X
train_stats = train_stats.transpose()  # 转置

# 将特征值从目标值或者"标签"中分离。 这个标签是你使用训练模型进行预测的值。
# 将MPG字段移出为标签数据： 移动 MPG 油耗效能这一列为真实标签 Y
train_labels = train_dataset.pop('MPG')
test_labels = test_dataset.pop('MPG')

"""
数据归一化
"""


# 标准化数据
def norm(x):  # 减去每个字段的均值，并除以标准差
    return (x - train_stats['mean']) / train_stats['std']


normed_train_data = norm(train_dataset)  # 标准化训练集
normed_test_data = norm(test_dataset)  # 标准化测试集
# 打印出训练集和测试集的大小：
print(normed_train_data.shape, train_labels.shape)
print(normed_test_data.shape, test_labels.shape)

# (314, 9)(314, )  # 训练集共 314 行，输入特征长度为 9,标签用一个标量表示
# (78, 9)(78, )  # 测试集共 78 行，输入特征长度为 9,标签用一个标量表示


"""
构建模型
"""


def build_model():
    model = keras.Sequential([
        layers.Dense(64, activation='relu', input_shape=[len(train_dataset.keys())]),
        layers.Dense(64, activation='relu'),
        layers.Dense(1)
    ])

    optimizer = tf.keras.optimizers.RMSprop(0.001)

    model.compile(loss='mse',
                  optimizer=optimizer,
                  metrics=['mae', 'mse'])
    return model


model = build_model()
# 打印网络信息
model.summary()

# 现在试用下这个模型。从训练数据中批量获取‘10’条例子并对这些例子调用 model.predict
example_batch = normed_train_data[:10]
example_result = model.predict(example_batch)
print("example_result：{example_result}\n".format(example_result=example_result))

"""
训练模型
"""


# 通过为每个完成的时期打印一个点来显示训练进度
class PrintDot(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs):
        if epoch % 100 == 0: print('')
        print('.', end='')


# 对模型进行100个周期的训练，并在 history 对象中记录训练和验证的准确性。
epochs = 100
history = model.fit(
    normed_train_data, train_labels,
    epochs=epochs, validation_split=0.2, verbose=0,
    callbacks=[PrintDot()])

# 使用 history 对象中存储的统计信息可视化模型的训练进度。
hist = pd.DataFrame(history.history)
hist['epoch'] = history.epoch
hist.tail()


def plot_history(history):
    hist = pd.DataFrame(history.history)
    hist['epoch'] = history.epoch

    plt.figure()
    plt.xlabel('Epoch')
    plt.ylabel('Mean Abs Error [MPG]')
    plt.plot(hist['epoch'], hist['mae'],
             label='Train Error')
    plt.plot(hist['epoch'], hist['val_mae'],
             label='Val Error')
    plt.ylim([0, 5])
    plt.legend()

    plt.figure()
    plt.xlabel('Epoch')
    plt.ylabel('Mean Square Error [$MPG^2$]')
    plt.plot(hist['epoch'], hist['mse'],
             label='Train Error')
    plt.plot(hist['epoch'], hist['val_mse'],
             label='Val Error')
    plt.ylim([0, 20])
    plt.legend()
    plt.show()


plot_history(history)

"""
模型优化
"""

# 我们将使用一个 EarlyStopping callback 来测试每个 epoch 的训练条件。如果经过一定数量的 epochs 后没有改进，则自动停止训练。
model = build_model()
# patience 值用来检查改进 epochs 的数量
early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=10)
history = model.fit(normed_train_data, train_labels, epochs=epochs,
                    validation_split=0.2, verbose=0, callbacks=[early_stop, PrintDot()])

plot_history(history)

"""
模型评估
"""
loss, mae, mse = model.evaluate(normed_test_data, test_labels, verbose=2)
print("Testing set Mean Abs Error: {:5.2f} MPG".format(mae))

# 绘制图像
test_predictions = model.predict(normed_test_data).flatten()

plt.scatter(test_labels, test_predictions)
plt.xlabel('True Values [MPG]')
plt.ylabel('Predictions [MPG]')
plt.axis('equal')
plt.axis('square')
plt.xlim([0, plt.xlim()[1]])
plt.ylim([0, plt.ylim()[1]])
_ = plt.plot([-100, 100], [-100, 100])
plt.show()

# 这看起来我们的模型预测得相当好。我们来看下误差分布。
error = test_predictions - test_labels
plt.hist(error, bins=25)
plt.xlabel("Prediction Error [MPG]")
_ = plt.ylabel("Count")
plt.show()
