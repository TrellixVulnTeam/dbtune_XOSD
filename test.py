# shutil.copy2('client/driver/conf/driver_config_template.py', 'client/driver/conf/111-driver_config.py')
#
# path = 'client.driver.conf.111-driver_config'
# module = importlib.import_module(path)
# # 执行脚本功能
# # func = module.poc('')
#
#
# print(module.__name__)
# # 获取脚本描述信息
# print(module.DRIVER_HOME)
#
# module.DRIVER_HOME = 'test'
#
# print(module.DRIVER_HOME)
from urllib.parse import quote_plus, unquote_plus

import pika

# BROKER_URL = 'amqp://admin:dameng@777@192.168.113.145:5691//'
CELERY_APP_QUEUE = 'tuneTopic.cdb-server-biz'

# host_ip = BROKER_URL.split("@")[-1].replace("//","")
# hostname = host_ip.split(':')[0]
# port = host_ip.split(':')[1]
user = 'admin'
hostname = '192.168.113.145'
# user = 'guest'
# hostname = '192.168.144.152'
# port = '5672'
port = '5691'
pwd = quote_plus('dameng@777')
BROKER_URL = 'amqp://{}:{}@{}:{}//'.format(user, pwd, hostname, port)

# protocol = BROKER_URL.split('//')[1]
# user = protocol.split('@')[0].split(":")[0]
# pwd = protocol.split('@')[0].split(":")[1]
# host_ip = protocol.split('"')[-1].split('@')[1]
# hostname = host_ip.split(':')[0]
# port = host_ip.split(':')[1].split('/')[0]

host_ip = BROKER_URL.split("@")[-1].replace("//", "")
hostname = host_ip.split(':')[0]
port = host_ip.split(':')[1]

pwd = unquote_plus(pwd)
credentials = pika.PlainCredentials(user, pwd)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname,
                                                               port=int(port),
                                                               virtual_host='/',
                                                               credentials=credentials))

channel = connection.channel()

topic = CELERY_APP_QUEUE.split(".")[0]

# 声明一个名为direct_logs类型为direct的exchange
# 同时在producer和consumer中声明exchage或queue是个好习惯，以保证其存在
channel.exchange_declare(exchange=topic,
                         exchange_type='topic', durable=True)

result = channel.queue_declare(queue=CELERY_APP_QUEUE, exclusive=False, durable=True,
                               arguments={'x-message-ttl': 600000, 'x-dead-letter-exchange': 'DLX',
                                          'x-dead-letter-routing-key': CELERY_APP_QUEUE})
queue_name = result.method.queue

# exchange和queue之间的binding可接受routing_key参数
# fanout类型的exchange直接忽略该参数。direct类型的exchange精确匹配该关键字进行message路由
# 一个消费者可以绑定多个routing_key
# Exchange就是根据这个RoutingKey和当前Exchange所有绑定的BindingKey做匹配，
# 如果满足要求，就往BindingKey所绑定的Queue发送消息
channel.queue_bind(exchange=topic,
                   queue=queue_name,
                   routing_key=CELERY_APP_QUEUE,
                   arguments={'x-message-ttl': 600000, 'x-dead-letter-exchange': 'DLX',
                              'x-dead-letter-routing-key': CELERY_APP_QUEUE})


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body,))


channel.basic_consume(queue=queue_name,
                      on_message_callback=callback,
                      auto_ack=True)

channel.start_consuming()

# # 定义一个回调函数来处理消息队列中的消息，这里是打印出来
# def callback(ch, method, properties, body):
#     # 手动发送确认消息
#     ch.basic_ack(delivery_tag=method.delivery_tag)
#     print(body.decode(encoding='UTF-8'))
#
#
# def coms():
#     channel = connection.channel()
#     # 申明消息队列。当不确定生产者和消费者哪个先启动时，可以两边重复声明消息队列。
#     channel.queue_declare(queue=CELERY_APP_QUEUE, durable=True)
#     # 告诉生产者，消费者已收到消息
#     # 告诉rabbitmq，用callback来接收消息
#     # 默认情况下是要对消息进行确认的，以防止消息丢失。
#     # 此处将auto_ack明确指明为True，不对消息进行确认。
#     channel.basic_consume(CELERY_APP_QUEUE,
#                           on_message_callback=callback)
#     # auto_ack=True)  # 自动发送确认消息
#     # 开始接收信息，并进入阻塞状态，队列里有信息才会调用callback进行处理
#     channel.start_consuming()
#
#
# if __name__ == '__main__':
#     coms()
