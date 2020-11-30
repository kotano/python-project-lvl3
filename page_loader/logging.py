import logging
import os
import sys
from functools import wraps
from logging.handlers import RotatingFileHandler


FORMATTER = logging.Formatter(
    '%(asctime)s %(name)-24s %(levelname)-8s %(message)s')

LOG_FILE = os.path.join(
    os.environ['LOCALAPPDATA' if 'win' in sys.platform else 'HOME'],
    'page_loader', 'page_loader.log')


def configure_logger(level="WARNING"):
    lvl = logging.getLevelName(level.upper())
    if not os.path.exists(os.path.dirname(LOG_FILE)):
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=False)

    logging.basicConfig(
        format=FORMATTER,
        # filename=LOG_FILE,
        level=lvl,
        handlers=[get_file_handler(lvl), get_console_handler(lvl)],
    )
    logging.debug("Logger is configured")
    return logging.getLogger()


def get_console_handler(level):
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler(level):
    file_handler = RotatingFileHandler(LOG_FILE, 'a', 2**20, 4)
    file_handler.setFormatter(FORMATTER)
    return file_handler


logger = logging.getLogger('logger')


def log_func(function):

    @wraps(function)
    def inner(*args, **kwargs):
        logger.debug("{:<<20} IN {} {}".format(
            function.__name__, args, kwargs))
        res = function(*args, **kwargs)
        logger.debug("{:><20} OUT {}".format(function.__name__, res))
        return res

    return inner
