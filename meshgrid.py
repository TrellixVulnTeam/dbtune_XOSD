import matplotlib
from matplotlib import pyplot as plt
# 导入 3D 坐标轴支持
from mpl_toolkits.mplot3d import Axes3D
import tensorflow as tf

x = tf.linspace(-8., 8, 100)  # 设置 x 轴的采样点
y = tf.linspace(-8., 8, 100)  # 设置 y 轴的采样点
x, y = tf.meshgrid(x, y)  # 生成网格点，并内部拆分后返回
print(x.shape, y.shape)  # 打印拆分后的所有点的 x,y 坐标张量 shape

z = tf.sqrt(x ** 2 + y ** 2)
z = tf.sin(z) / z  # sinc 函数实现

# 通过 matplotlib 库即可绘制出函数在𝑦 ∈ [−8,8],𝑧 ∈ [−8,8]区间的 3D 曲面
fig = plt.figure()
ax = Axes3D(fig)  # 设置 3D 坐标轴
# 根据网格点绘制 sinc 函数 3D 曲面
ax.contour3D(x.numpy(), y.numpy(), z.numpy(), 50)
plt.show()
