import logging

import pika

logger = logging.getLogger(__name__)
# import sys
from retrying import retry


class RabbitmqServer(object):
    def __init__(self, username, password, serverip, port, virtual_host):
        self.username = username
        self.password = password
        self.serverip = serverip
        self.port = port
        self.virtual_host = virtual_host

    # def connent(self):
    #    for i in range(3):
    #         try:
    #             logger.info("into mq connet")
    #             user_pwd = pika.PlainCredentials(self.username,self.password)
    #             logger.info("create mq ...")
    #             logger.info("%s,%s,%s,%s,%s"%(self.virtual_host,self.serverip,self.port,self.password,self.username))
    #             s_conn = pika.BlockingConnection(pika.ConnectionParameters(virtual_host=self.virtual_host,host= self.serverip,port=self.port, credentials=user_pwd))  # 创建连接
    #             logger.info('create channel...')
    #             self.channel = s_conn.channel()
    #             logger.info('connect successful')
    #             break
    #         except Exception as e:
    #             logger.info("连接mq失败，沉睡10s再试，共沉睡三次,失败原因:%s",e)
    #             time.sleep(10)
    @retry(stop_max_delay=30000, wait_fixed=5000)
    def connect(self):
        logger.info("into mq connect")
        user_pwd = pika.PlainCredentials(self.username, self.password)
        logger.info("create mq ...")
        logger.info("%s,%s,%s,%s,%s" % (self.virtual_host, self.serverip, self.port, self.password, self.username))
        # 创建 mq连接
        s_conn = pika.BlockingConnection(
            pika.ConnectionParameters(virtual_host=self.virtual_host, host=self.serverip, port=self.port,
                                      credentials=user_pwd))
        self.conn = s_conn
        logger.info('create channel...')
        self.channel = s_conn.channel()
        logger.info('connect successful')

    def productMessage(self, queue, message):
        topic_exchange = queue.split(".")[0]
        # topic类型的exchange
        self.channel.exchange_declare(exchange=topic_exchange,
                                      exchange_type='topic', durable=True)
        # self.channel.queue_declare(queue=queue, durable=True)
        # self.channel.basic_publish(exchange='',
        #                            routing_key=queue,  # 写明将消息发送给队列queuename
        #                            body=message)
        self.channel.basic_publish(exchange=topic_exchange,
                                   routing_key=queue,  # 写明将消息发送给队列queuename
                                   body=message)

    def close(self):
        self.channel.close()
        self.conn.close()
