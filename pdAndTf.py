import pandas as pd
import tensorflow as tf

csv_file = tf.keras.utils.get_file('heart.csv', 'https://storage.googleapis.com/applied-dl/heart.csv')

df = pd.read_csv(csv_file)

df.head()

print("{dtypes} \n".format(dtypes=df.dtypes))

df['thal'] = pd.Categorical(df['thal'])
df['thal'] = df.thal.cat.codes

print(df.head())

# 使用 tf.data.Dataset 读取pandas dataframe数据

target = df.pop('target')
dataset = tf.data.Dataset.from_tensor_slices((df.values, target.values))
for feat, targ in dataset.take(5):
    print('Features: {}, Target: {}'.format(feat, targ))

tf.constant(df['thal'])

train_dataset = dataset.shuffle(len(df)).batch(1)


# 创建并训练模型
def get_compiled_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(10, activation='relu'),
        tf.keras.layers.Dense(10, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    return model


model = get_compiled_model()
model.fit(train_dataset, epochs=15)

# 将字典作为输入传输给模型就像创建 tf.keras.layers.Input 层的匹配字典一样简单，应用任何预处理并使用 functional api。
# 您可以使用它作为 feature columns 的替代方法。
inputs = {key: tf.keras.layers.Input(shape=(), name=key) for key in df.keys()}
x = tf.stack(list(inputs.values()), axis=-1)

x = tf.keras.layers.Dense(10, activation='relu')(x)
output = tf.keras.layers.Dense(1, activation='sigmoid')(x)

model_func = tf.keras.Model(inputs=inputs, outputs=output)

model_func.compile(optimizer='adam',
                   loss='binary_crossentropy',
                   metrics=['accuracy'])

# 与 tf.data 一起使用时，保存 pd.DataFrame 列结构的最简单方法是将 pd.DataFrame 转换为 dict ，并对该字典进行切片。
dict_slices = tf.data.Dataset.from_tensor_slices((df.to_dict('list'), target.values)).batch(16)

for dict_slice in dict_slices.take(1):
    print(dict_slice)

model_func.fit(dict_slices, epochs=15)
