#coding:utf-8
import logging
import logging.handlers
import os
from config import Config

class Log:
    logger = None
    @staticmethod
    def getLogger():
        if Log.logger is not None:
            return Log.logger
        Log.logger = logging.getLogger()
        Log.logger.setLevel(Config.LOG_LEVEL)
        Rthandler = logging.handlers.RotatingFileHandler(
                Config.LOG_FILE_PATH,
                maxBytes=Config.LOG_MAX_SIZE,
                backupCount=Config.LOG_BACKUP_COUNT,
                )
        StreamHandler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s-[%(levelname)s][%(module)s][%(funcName)s]-%(message)s')
        Rthandler.setFormatter(formatter)
        StreamHandler.setFormatter(formatter)
        Rthandler.setLevel(Config.FILE_LOG_LEVEL)
        StreamHandler.setLevel(Config.STREAM_LOG_LEVEL)
        Log.logger.addHandler(Rthandler)
        Log.logger.addHandler(StreamHandler)
        return Log.logger
