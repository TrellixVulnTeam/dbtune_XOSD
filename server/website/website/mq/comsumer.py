# # 消费者代码
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
# credentials = pika.PlainCredentials(user, pwd)
# connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname,
#                                                                port=port,
#                                                                virtual_host='/',
#                                                                credentials=credentials))
#
# channel = connection.channel()
# # 申明消息队列。当不确定生产者和消费者哪个先启动时，可以两边重复声明消息队列。
# channel.queue_declare(queue=CELERY_APP_QUEUE, durable=False)
#
#
# # 定义一个回调函数来处理消息队列中的消息，这里是打印出来
# def callback(ch, method, properties, body):
#     # 手动发送确认消息
#     ch.basic_ack(delivery_tag=method.delivery_tag)
#     print(body.decode())
#     # 告诉生产者，消费者已收到消息
#
#
# # 告诉rabbitmq，用callback来接收消息
# # 默认情况下是要对消息进行确认的，以防止消息丢失。
# # 此处将auto_ack明确指明为True，不对消息进行确认。
# channel.basic_consume(CELERY_APP_QUEUE,
#                       on_message_callback=callback)
# # auto_ack=True)  # 自动发送确认消息
# # 开始接收信息，并进入阻塞状态，队列里有信息才会调用callback进行处理
# channel.start_consuming()
