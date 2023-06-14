import logging
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler
import re


class BaseConfig(object):
    OpenAIKey = "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"
    PineconeAPIKey = "06420329-37da-4628-b0a8-0472e1fffcd5"
    IndexName = "chatbang"
    Environment = "asia-southeast1-gcp-free"
    OpenAI_URL = ""

    def setup_log(self):
        # 设置日志的记录等级
        logging.basicConfig(level=logging.INFO, filename="logs/info.log", filemode="a")  # 调试debug级
        # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
        # file_log_handler = RotatingFileHandler("logs/log.log", maxBytes=1024 * 1024 * 100, backupCount=10)
        file_log_handler = TimedRotatingFileHandler("logs/info.log", when='D', interval=1, backupCount=7,
                                                    encoding='utf-8')
        file_log_handler.suffix = '%Y-%m-%d.log'
        file_log_handler.extMatch = re.compile(r'^\d{4}-\d{2}-\d{2}.log')
        # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
        formatter = logging.Formatter('%(asctime)s - %(levelname)s %(filename)s:%(lineno)d %(message)s')
        # 为刚创建的日志记录器设置日志记录格式
        file_log_handler.setFormatter(formatter)
        # 为全局的日志工具对象（flask app使用的）添加日志记录器
        logging.getLogger().addHandler(file_log_handler)

        logging.basicConfig(level=logging.ERROR, filename="logs/error.log", filemode="a")  # 调试debug级
        # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
        # file_log_handler = RotatingFileHandler("logs/error.log", maxBytes=1024 * 1024 * 10)
        error_log_handler = TimedRotatingFileHandler("logs/error.log", when='D', interval=1, backupCount=7,
                                                     encoding='utf-8')
        error_log_handler.suffix = '%Y-%m-%d.log'
        error_log_handler.extMatch = re.compile(r'^\d{4}-\d{2}-\d{2}.log')
        # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
        error_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s %(filename)s-%(funcName)s:%(lineno)d %(message)s')
        # 为刚创建的日志记录器设置日志记录格式
        error_log_handler.setFormatter(error_formatter)
        # 为全局的日志工具对象（flask app使用的）添加日志记录器
        logging.getLogger().addHandler(error_log_handler)


class ProdConfig(BaseConfig):
    pass


config = BaseConfig()
