"""
The NUM_CODE is length of authentication
"""
NUM_OF_CODE = 8

"""
You should configure your data base here!
"""
DB_TYPE = 'mysql'
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'tianxunceshi'
DB_PORT = 3306
DB_NAME = 'sqlalchemy_demo'

# The basic configuration class holds common settings, overloaded
# in subclasses as necessary.

import os
from hokey.configbase import ConfigBase


class DevelopmentConfig(ConfigBase):

    MAIN_SPLIT = ['head_tag/1', 'message_id/2', 'msg_attr/2',
                  'device_id/6', 'msg_product/2',
                  'package_item/is_subpackage(msg_attr)?13~15:13~13',
                  'content/is_subpackage(msg_attr)?15~-2:13~-2',
                  'crc/-2~-1'
                  ]

    MESSAGE_ID = 'message_id'
    DEVICE_ID = 'device_id'
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 't0p s3cr3t'
    HOST = '0.0.0.0'
    PORT = 5555
    ESCAPE_LIST = {'0x7e7b': '0x7e', '0x7b7b': '0x7b'}


class TestingConfig(ConfigBase):
    pass


class ProductConfig(ConfigBase):
    pass
