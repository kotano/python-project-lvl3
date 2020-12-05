import os
import sys
import logging
from functools import wraps

from logging.handlers import RotatingFileHandler


FORMATTER = logging.Formatter(
    '%(asctime)s %(name)-24s %(levelname)-8s %(message)s')

LOG_FILE = os.path.join(
    os.environ['LOCALAPPDATA' if 'win' in sys.platform else 'HOME'],
    'page_loader', 'page_loader.log')


class PageLoaderError(BaseException):
    pass


class PathAccessError(PageLoaderError):
    pass


class ConnectionError(PageLoaderError):
    pass


def configure_logger(level="INFO"):
    lvl = logging.getLevelName(level.upper())

    logging.basicConfig(
        level=lvl,
        handlers=[
            get_file_handler(),
            get_error_console_handler(),
            get_standard_console_handler()])
    logging.debug("Logger is configured")
    return logging.getLogger()


def get_error_console_handler():
    formatter = logging.Formatter('%(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.ERROR)
    return console_handler


def get_standard_console_handler():
    formatter = logging.Formatter('%(message)s')
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    handler.setLevel(0)
    handler.addFilter(lambda record: record.levelno <= logging.WARNING)
    return handler


def get_file_handler():
    dirname = os.path.dirname(LOG_FILE)
    if not os.path.exists(dirname):
        os.path.makedirs(dirname)
    file_handler = RotatingFileHandler(LOG_FILE, 'a', 2**20, 4)
    file_handler.setFormatter(FORMATTER)
    return file_handler


logger = logging.getLogger('fixture')


def log_func(func):
    @wraps(func)
    def inner(*args, **kwargs):
        logger.debug("{:<<20} IN {} {}".format(
            func.__name__, args, kwargs))
        res = func(*args, **kwargs)
        logger.debug("{:><20} OUT {}".format(func.__name__, res))
        return res
    return inner


# TODO
def error_handler(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
        except OSError as e:
            logger.exception(e)
            exit(1)
        else:
            return res
    return inner
