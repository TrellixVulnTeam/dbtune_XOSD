# coding:utf-8
import logging
from logging.handlers import TimedRotatingFileHandler

import colorlog  # 控制台日志输入颜色

log_colors_config = {
    'DEBUG': 'cyan',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red',
}


# 单例模式
class Log(object):
    __flag = None

    def __new__(cls, *args, **kwargs):
        if not cls.__flag:
            cls.__flag = super().__new__(cls)
        return cls.__flag

    def __init__(self, log_name: str = '/opt/test.log', level=logging.INFO):
        if 'logger' not in self.__dict__:
            logger = logging.getLogger()
            logger.setLevel(level)
            filehandle = logging.FileHandler(log_name, encoding='utf-8')
            streamhandle = logging.StreamHandler()
            logger.addHandler(filehandle)
            logger.addHandler(streamhandle)
            self.formatter = colorlog.ColoredFormatter(
                '%(log_color)s[%(asctime)s] [%(filename)s:%(lineno)d] [%(levelname)s] %(message)s',
                log_colors=log_colors_config)
            filehandle.setFormatter(self.formatter)
            streamhandle.setFormatter(self.formatter)
            self.logger = logger

    def return_logger(self):
        return self.logger


def get_logger(log_name: str = '/opt/test.log', level=logging.INFO):
    return Log(log_name, level).return_logger()


if __name__ == '__main__':
    log = get_logger()
    log.debug('test')
    log.warning('test')
    log.info('Wait %s seconds after restarting database', 1)

# class Log:
#     def __init__(self, logname: str = '/opt/test.log', code=None):
#         self.logname = logname
#         self.code = code
#         self.logger = logging.getLogger()
#         self.logger.setLevel(logging.DEBUG)
#         self.formatter = colorlog.ColoredFormatter(
#             '%(log_color)s[%(asctime)s] [%(filename)s:%(lineno)d] [' + code + '] [%(levelname)s]- %(message)s',
#             log_colors=log_colors_config)
#
#         # FileHandler = RotatingFileHandler(  # pylint: disable=invalid-name
#         #     self.logname, maxBytes=50000, backupCount=2)
#         # 创建一个 FileHandler，写到本地
#         fh = TimedRotatingFileHandler(
#             self.logname, when='MIDNIGHT', interval=1, encoding='utf-8')
#         fh.setLevel(logging.DEBUG)
#         fh.setFormatter(self.formatter)
#         self.logger.addHandler(fh)
#
#         # 创建一个StreamHandler,写到控制台
#         ch = logging.StreamHandler()
#         ch.setLevel(logging.DEBUG)
#         ch.setFormatter(self.formatter)
#         self.logger.addHandler(ch)
#
#     def console(self, level: str, message: str):
#         LV = {
#             'debug': self.logger.debug,
#             'info': self.logger.info,
#             'warn': self.logger.warning,
#             'error': self.logger.error,
#             'critical': self.logger.critical
#         }
#         f = LV.get(level, self.debug)
#         f(message)
#
#     def debug(self, message):
#         self.console('debug', message)
#
#     def info(self, message):
#         self.console('info', message)
#
#     def warning(self, message):
#         self.console('warning', message)
#
#     def error(self, message):
#         self.console('error', message)
#
#     def critical(self, message):
#         self.console('critical', message)
#
#
# if __name__ == "__main__":
#     log = Log()
#     log.info("测试1")
#     log.debug("测试2")
#     log.warning("warning")
#     log.error("error")
#     log.critical("critical")
