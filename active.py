import tensorflow as tf

x = tf.linspace(-6., 6., 10)

# 把𝑦 ∈ 𝑆的输入“压缩”到𝑦 ∈ (0,1)区间
y = tf.nn.sigmoid(x)  # 通过 Sigmoid 函数

print("{x} \n {y}".format(x=x, y=y))

# ReLU 对小于 0 的值全部抑制为 0；对于正数则直接输出，这种单边抑制特性来源于生物学
tf.nn.relu(x)  # 通过 ReLU 激活函数

# 当𝑞 = 0时，LeayReLU 函数退化为 ReLU 函数；当𝑞 ≠ 0时，𝑦 < 0处能够获得较小的导数值𝑞
tf.nn.leaky_relu(x, alpha=0.1)  # 通过 LeakyReLU 激活函数

# 能够将𝑦 ∈ 𝑆的输入“压缩”到(−1,1)区间
tf.nn.tanh(x)
