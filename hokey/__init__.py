# from .core import Hokey
from convert import ConvertBase, SplitBase
# for import easy easy
# from swi import main_split
from tools import is_subpackage, is_encryption, is_complete
from template import render
from core import Hokey


# Default convert function define below
@ConvertBase.register_convert_func('to_word')
def to_double_fun(val):
    print 'hello'


@ConvertBase.register_convert_func('to_double')
def to_double_fun(val):
    print 'hello'


@ConvertBase.register_convert_func('to_dword')
def to_double_fun(val):
    print 'hello'


@ConvertBase.register_convert_func('to_bcd')
def to_double_fun(val):
    print 'hello'


# --------------------------------------------------
@SplitBase.register_rely_func('is_sub')
def is_subpackage_fun(val):
    return is_subpackage(val)


@SplitBase.register_rely_func('is_encryption')
def is_encryption_fun(val):
    return is_encryption(val)


if __name__ == '__main__':
    # Test convert_base instance
    print 'Convert.convert_function', ConvertBase.convert_functions
