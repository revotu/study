# -*-encoding: utf-8 -*-
#
# @author zengbaoqing
#
# Nov 2017

import logging.config
import os
from datetime import datetime
import socket

hostname = socket.gethostname()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEFAULT_SERVER_PORT = 8190

if hostname.startswith('ali-prod'):
    env = 'prod'
    debug = False
    cache = True

elif hostname.startswith('vpc-prod'):
    env = 'prod'
    debug = False
    cache = True


elif hostname.startswith('ali-stable'):
    env = 'stable'
    debug = False
    cache = True

elif hostname.startswith('ali-test'):
    env = 'test'
    debug = False
    cache = False
else:
    env = 'dev'
    debug = True
    cache = True

# Logging conifg

LOG_FILE_PATH = '/mnt/logs/anchor-rpc-%s.log' % datetime.now().strftime('%Y-%m-%d')

if env == 'dev':
    LOG_FILE_PATH = os.path.join(BASE_DIR, 'anchor/temp/%s-index.log' % datetime.now().strftime('%Y-%m-%d'))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(message)s'
        },
        'precise': {
            'format': '%(levelname)s \x1b[6;30;42m%(asctime)s\x1b[0m %(name)s \x1b[1;32;40m%(message)s\x1b[0m\n'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILE_PATH,  # 日志输出文件
            'maxBytes': 1024 * 1024 * 5,  # 文件大小
            'backupCount': 5,  # 备份份数
            'formatter': 'standard',  # 使用哪种formatters日志格式
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILE_PATH,
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'precise'
        },
        'request_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILE_PATH,
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'scprits_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILE_PATH,
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'standard',
        }
    },
    'loggers': {
        'rpc': {
            'handlers': ['default', 'console'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('rpc')
