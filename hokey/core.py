from convert import ConvertBase, SplitBase, SplitConvertBase
from _tools import is_subpackage, is_encryption


# Default convert function define below
@ConvertBase.register_convert_func('to_bcd')
def to_bcd(val):
    temp_hex = []
    for item in val:
        temp_hex.append(hex(item))
    temp_str = ''
    for item in temp_hex:
        temp_str += str(item).replace('0x', '')
    return temp_str


def to_dword(val):
    """
    :param val: a tuple (2, 110, 226, 147)
    :return:40821395 but what we need is range(38.0000 ~ 42.00000)
    """
    temp_hex = []
    for item in val:
        temp_hex.append(hex(item))
    temp_str = ''
    for item in temp_hex:
        temp_str += str(item).replace('0x', '')
    result = int(temp_str, 16)
    return result


@ConvertBase.register_convert_func('to_dword')
def to_double_word_fun(val):
    """
    :param val: a tuple (2, 110, 226, 147)
    :return: (38.0000 ~ 42.00000)
    """
    a_value = to_dword(val)
    temp = float(a_value)
    ret = temp / 1000000
    return ret


@ConvertBase.register_convert_func('to_int')
def to_int_dword_fun(val):
    a_value = to_dword(val)
    temp = int(a_value)
    return temp


@ConvertBase.register_convert_func('to_word')
def to_a_word_fun(val):
    """
    :param val: a tuple with two element (2, 110)
    :return:
    """
    a_value = to_dword(val)
    temp = float(a_value)
    return temp


# --------------------------------------------------
@SplitBase.register_rely_func('is_sub')
def is_subpackage_fun(val):
    return is_subpackage(val)


@SplitBase.register_rely_func('is_encryption')
def is_encryption_fun(val):
    return is_encryption(val)


if __name__ == '__main__':
    # Test convert_base instance
    # print 'Convert.convert_function', ConvertBase.convert_functions
    class SampleSplitConvertBase(SplitConvertBase):
        crc_check = False
        sub_split_rule = ['message_id/2', 'message_attr/2 | to_int', 'device/6 | to_bcd',
                          'product/2 | to_int', 'content/4 | to_dword']


    sample = (1, 0, 0, 2, 1, 80, 51, 80, 68, 118, 0, 1, 2, 110, 226, 147, 5)
    result = SampleSplitConvertBase(sample)
    print result.result
