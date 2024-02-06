import os
import logging
import time
from logging.handlers import RotatingFileHandler

# 日志保存路径
log_dir_name = "D:" + os.sep+"logs"


def getLogHandler():
    # 文件名，以日期作为文件名
    log_file_name = 'logger-' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.log'
    # 创建日志文件
    log_file_str = log_dir_name + os.sep + log_file_name
    # 默认日志等级的设置,注意打印日志时，只会打印默认等级以上的
    logging.basicConfig(level=logging.INFO)
    # 创建日志记录器，指明日志保存路径,每个日志的大小，保存日志的上限
    file_log_handler = RotatingFileHandler(log_file_str, maxBytes=1024 * 1024, backupCount=10, encoding='UTF-8')
    # 设置日志的格式                   发生时间    日志等级     日志信息文件名      函数名          行数        日志信息
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    # 将日志记录器指定日志的格式
    file_log_handler.setFormatter(formatter)

    return file_log_handler
