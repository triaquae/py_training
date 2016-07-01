#_*_coding:utf-8_*_
__author__ = 'Alex Li'


import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SALT_MASTER = 'localhost'


FILE_SERVER = {
    'http':'%s:8000' %SALT_MASTER.strip(),
    'salt':SALT_MASTER
}
FILE_SREVER_BASE_PATH = '/salt/file_center'

FILE_STORE_PATH = "%s/var/downloads/" % BASE_DIR

#tmp config
NEEDLE_CLIENT_ID =  1

MQ_CONN = {
    'host':'localhost',
    'port': 4000,
    'password': ''
}

