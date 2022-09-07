# # 生产者代码
# import pika
#
# from server.website.website.settings import BROKER_URL, CELERY_APP_QUEUE
#
# protocol = BROKER_URL.split('@')[0]
# user = protocol.split('//')[1].split(':')[0]
# pwd = protocol.split('//')[1].split(':')[1]
# url = BROKER_URL.split('@')[-1]
# hostname = url.split(':')[0]
# port = url.split(':')[1].split('/')[0]
#
# credentials = pika.PlainCredentials(user, pwd)  # mq用户名和密码，没有则需要自己创建
# # 虚拟队列需要指定参数 virtual_host，如果是默认的可以不填。
# connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname,
#                                                                port=port,
#                                                                virtual_host='/',
#                                                                credentials=credentials))
#
# # 建立rabbit协议的通道
# channel = connection.channel()
# # 声明消息队列，消息将在这个队列传递，如不存在，则创建。durable指定队列是否持久化
# channel.queue_declare(queue=CELERY_APP_QUEUE, durable=False)
#
# # message不能直接发送给queue，需经exchange到达queue，此处使用以空字符串标识的默认的exchange
# # 向队列插入数值 routing_key是队列名
# channel.basic_publish(exchange='',
#                       routing_key='python-test',
#                       body='Hello world！2')
# # 关闭与rabbitmq server的连接
# connection.close()
from urllib.parse import unquote_plus

from .mqserver import RabbitmqServer
from website.settings import BROKER_URL, CELERY_APP_QUEUE


def push_msg(msg):
    protocol = BROKER_URL.split('@')[0]
    user = protocol.split('//')[1].split(':')[0]
    pwd = protocol.split('//')[1].split(':')[1]
    url = BROKER_URL.split('@')[-1]
    hostname = url.split(':')[0]
    port = url.split(':')[1].split('/')[0]
    mq_server = RabbitmqServer(username=user, password=unquote_plus(pwd), serverip=hostname, port=port, virtual_host='/')
    mq_server.connect()
    mq_server.productMessage(CELERY_APP_QUEUE, msg)
    mq_server.close()
