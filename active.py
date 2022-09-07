# import tensorflow as tf
#
# x = tf.linspace(-6., 6., 10)
#
# # 把𝑦 ∈ 𝑆的输入“压缩”到𝑦 ∈ (0,1)区间
# y = tf.nn.sigmoid(x)  # 通过 Sigmoid 函数
#
# print("{x} \n {y}".format(x=x, y=y))
#
# # ReLU 对小于 0 的值全部抑制为 0；对于正数则直接输出，这种单边抑制特性来源于生物学
# tf.nn.relu(x)  # 通过 ReLU 激活函数
#
# # 当𝑞 = 0时，LeayReLU 函数退化为 ReLU 函数；当𝑞 ≠ 0时，𝑦 < 0处能够获得较小的导数值𝑞
# tf.nn.leaky_relu(x, alpha=0.1)  # 通过 LeakyReLU 激活函数
#
# # 能够将𝑦 ∈ 𝑆的输入“压缩”到(−1,1)区间
# tf.nn.tanh(x)


# import itertools
# import re
# import math
#
# import pika
#
# lis = [0, 1, 2, 4, 8]
# # lis = [0, 1, 2, 4, 8, 16, 32]
#
# newLis = []
#
# a = True
# if a:
#     print(1)
# else:
#     print(0)
# for index in range(len(lis) - 1):
#     print(index)
#     array = list(itertools.combinations(list(lis), 2 + index))
#     print("排列组合结果===>  组合总数：{count} 详细结果：{array}\n".format(count=len(array), array=array))
#
#     for i in array:
#         total = sum(i)
#         newLis.append(total)
#         print("{i} 两两相加结果: {total}".format(i=i, total=total))
#
# print("newLis: {newLis}".format(newLis={}.fromkeys(newLis).keys()))


# array = list(itertools.combinations(list(lis), 2))
# print("排列组合结果===>  组合总数：{count} 详细结果：{array}\n".format(count=len(array), array=array))
#
# for i in array:
#     total = sum(i)
#     print("{i} 两两相加结果: {total}".format(i=i, total=total))
#
# searchObj = re.match(r'BASE_(.*)_CPU', "SCAN_CPU", re.M | re.I)
# if searchObj:
#     print("searchObj.group() : ", searchObj.group())
# else:
#     print("Nothing found!!")
#
#
# # 判断是否为素数
# def is_prime(number):
#     if number == 1:
#         return False
#     sqrt = int(math.sqrt(number))
#     for j in range(2, sqrt + 1):  # 从2到number的算术平方根迭代
#         if number % j == 0:  # 判断j是否为number的因数
#             return False
#     return True


# # 生成跟当前值最接近的素数
# def generate_prime(number):
#     for j in range(1, 3):  # 从2到number的算术平方根迭代
#         number = number + j
#         if is_prime(number):  # 判断j是否为number的因数
#             return number
#
#
# print(generate_prime(1))
#
# from string import Template
# import yaml
#
# with open("client/driver/conf/dm_driver_conf_template.yml", encoding='utf-8') as fp:
#     read_yml_str = fp.read()
#     # print(xx)
#
#     tempTemplate1 = Template(read_yml_str)
#     c = tempTemplate1.safe_substitute({"HOST_CONN": "1", "CONTAINER_NAME": "123456 "})
#     # print(c)
# fp.close()
#
# # yml 文件数据，转 python 类型
# yaml_data = yaml.safe_load(c)
# print(yaml_data)
# print(yaml_data[0]['host'])
# print(yaml_data[1]['db'])
# print(yaml_data[2]['driver'])
#
# # 转换成yml字符串并写入文件
# with open("test.yml", "w") as f:
#     yaml.dump(yaml_data, f)
import datetime
import json

import pika

BROKER_URL = 'amqp://guest:guest@192.168.144.152:5672//'
CELERY_APP_QUEUE = 'app'
protocol = BROKER_URL.split('@')[0]
user = protocol.split('//')[1].split(':')[0]
pwd = protocol.split('//')[1].split(':')[1]
url = BROKER_URL.split('@')[-1]
hostname = url.split(':')[0]
port = url.split(':')[1].split('/')[0]

credentials = pika.PlainCredentials(user, pwd)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname,
                                                               port=int(port),
                                                               virtual_host='/',
                                                               credentials=credentials))

channel = connection.channel()
# 申明消息队列。当不确定生产者和消费者哪个先启动时，可以两边重复声明消息队列。
channel.queue_declare(queue=CELERY_APP_QUEUE, durable=True)

for i in range(10):  # 生成10条消息
    message = json.dumps(
        {'id': "10000%s" % i, "amount": 100 * i, "name": "tony", "createtime": str(datetime.datetime.now())})
# message不能直接发送给queue，需经exchange到达queue，此处使用以空字符串标识的默认的exchange
# 向队列插入数值 routing_key是队列名
channel.basic_publish(exchange='',
                      routing_key=CELERY_APP_QUEUE,
                      body=message)
connection.close()
