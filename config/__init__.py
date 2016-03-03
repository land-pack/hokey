# The basic configuration class holds common settings, overloaded
# in subclasses as necessary.

import os
from hokey.configbase import ConfigBase


class DevelopmentConfig(ConfigBase):
    PREFIX = 'client_'
    MAIN_SPLIT = ['head_tag/1', 'msg_id/2', 'msg_attr/2',
                  'dev_id/6', 'msg_product/2',
                  'package_item/is_subpackage(msg_attr)?13~15:13~13',
                  'content/is_subpackage(msg_attr)?15~-2:13~-2',
                  'crc/-2~-1'
                  ]
    MESSAGE_ID = 'client_message_id'
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 't0p s3cr3t'
    HOST = '0.0.0.0'
    PORT = 5555
    ESCAPE_LIST = {'0x7e7b': '0x7e', '0x7b7b': '0x7b'}


class TestingConfig(ConfigBase):
    pass


class ProductConfig(ConfigBase):
    pass
