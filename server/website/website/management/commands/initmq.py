from urllib.parse import unquote_plus

from django.core.management.base import BaseCommand
from website.mq.mqserver import RabbitmqServer
from website.settings import BROKER_URL


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("init_mq", "开始初始化Rabbitmq队列")
        try:
            protocol = BROKER_URL.split('//')[1]
            user = protocol.split('@')[0].split(":")[0]
            pwd = protocol.split('@')[0].split(":")[1]
            host_ip = protocol.split('"')[-1].split('@')[1]
            hostname = host_ip.split(':')[0]
            port = host_ip.split(':')[1].split('/')[0]
            mqServer = RabbitmqServer(username=user, password=unquote_plus(pwd), serverip=hostname, port=port, virtual_host='/')
            mqServer.connect()
            print("init_mq", "初始化Rabbitmq队列成功")
        except Exception as e:
            print("init_mq", e, "队列初始化失败")
            raise e
