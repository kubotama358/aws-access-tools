# -*- coding: utf-8 -*-
from logging import getLogger
import logging.config
import yaml
import os
import inspect

LOGGER_NAME = "custom_logging01"
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
HOMEDIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__))))

# logging.config.dictConfig(yaml.load(open("utils/logging.yaml").read()))
logging.config.dictConfig(yaml.load(open(os.path.join(HOMEDIR, "logging.yaml")).read()))


class LogWrapper:

    logger = None
    extra = {}

    def __init__(self, name):
        self.logger = getLogger(name)
        self.logger.setLevel(LOG_LEVEL)

    def debug(self, msg, *args):
        extra = self.get_extra(inspect.stack()[1][0])
        self.logger.debug(msg, *args, extra=extra)

    def info(self, msg, *args):
        extra = self.get_extra(inspect.stack()[1][0])
        self.logger.info(msg, *args, extra=extra)

    def error(self, msg, *args):
        extra = self.get_extra(inspect.stack()[1][0])
        self.logger.error(msg, *args, extra=extra)

    def exception(self, msg, error, *args):
        extra = self.get_extra(inspect.stack()[1][0])
        self.logger.error(msg, *args, extra=extra)
        self.logger.exception(error, *args, extra=extra)

    def get_extra(self, frame):
        frame_info = inspect.getframeinfo(frame)
        file_name = frame_info[0]
        file_name = file_name[file_name.rfind('/') + 1:]
        extra = {
            "file_name": file_name,
            "func_name": frame_info[2],
            "line_no": frame_info[1]
        }
        return extra


def get_logger(name=LOGGER_NAME):
    return LogWrapper(name)
