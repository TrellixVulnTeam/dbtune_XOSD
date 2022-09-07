# import json
#
# from celery.utils.log import get_task_logger
# from django.contrib.auth.models import User
# from website.celery import app
#
# LOG = get_task_logger(__name__)
#
# CDB_FLAG = 'CDB'
# user = User.objects.get(username=CDB_FLAG)
#
#
# @app.task(bind=True, name='push_message')
# def push_message(msg):
#     """
#     推送消息至应用队列
#     :return:
#     """
#     return json.load(msg)
#
# # @app.task(bind=True, name='push_msg')
# # def push_msg(self):
# #     """
# #     推送消息至应用队列
# #     :return:
# #     """
# #     arr = []
# #     sessions = Session.objects.filter(user__username=user, project__name=CDB_FLAG)
# #     for session in sessions:
# #         # 先查询推送记录表，确定是否有推送过
# #         mp = MessagePush.objects.filter(session=session).first()
# #         if mp is None:
# #             # 查询所有的backup_data结果
# #             backups = BackupData.objects.all()
# #             for backup in backups:
# #                 # 上一条，小于本条的降序第一个即是上一条（推荐配置和TPS值对应）
# #                 result_qs = Result.objects.filter(id__lt=backup.id).all()
# #                 if result_qs.count() == 0: continue
# #                 result = result_qs.order_by("-id").first()
# #                 arr.append(gen_message_push(session, result, backup))
# #             return arr
# #         else:
# #             # 查询最新的一条推荐训练结果记录
# #             latest_result_qs = Result.objects.filter(session=session).first()
# #             if latest_result_qs is None: continue
# #             latest_result = latest_result_qs.latest('creation_time')
# #             # 上一条，小于本条的降序第一个即是上一条（推荐配置和TPS值对应）
# #             result_qs = Result.objects.filter(id__lt=latest_result.id).all()
# #             if result_qs.count() == 0: continue
# #             result = result_qs.order_by("-id").first()
# #             backup = BackupData.objects.filter(result=result).first()
# #             return gen_message_push(session, result, backup)
#
#
# # session_name 上一结果ID+时间 推送状态
#
# # msg.update(message='failed to get the next configuration!', status='FAILURE')
# # msg.update(message='Service not ready, failed to get the next configuration!', status='FAILURE')
#
# # 推送消息至队列
# # push_message.apply_async(queue=CELERY_APP_QUEUE, args=[msg])
#
#
# # def gen_message_push(session, result, backup):
# #     msg = dict(message='successfully recommended the configuration!', status='SUCCESS', id='', recommendation='',
# #                performance='')
# #     bench = json.loads(json.loads(backup.other)['user_defined_metrics'])['throughput']
# #     config = json.loads(result.next_configuration)
# #
# #     msg.update(id=session.name, recommendation=config['recommendation'], performance=bench['value'])
# #     message_push = MessagePush.objects.create(
# #         session=session,
# #         result=result,
# #         tps=bench['value'],
# #         push_time=now())
# #     message_push.save()
# #     return msg
