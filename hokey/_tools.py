"""
Working for make sure we got complete data!
By checking CRC we can make sure!
"""
import struct
import binascii


def name_as_tuple(val):
    """
    To make hexlify being a decimal
    :param val: '0x8100' or '8100'
    :return: '(128,1)'
    """
    if isinstance(val, str):
        val = val.replace('0x', '')
        val = binascii.unhexlify(val)
        data_length = len(val)
        s = struct.Struct('%iB' % data_length)
        temp = s.unpack(val)
        return str(temp)
    else:
        raise TypeError("Except a String input!")


def check(a_tuple):
    flag = True
    check_code = 1
    temp = a_tuple[:-1]
    for each in temp:
        if flag:
            check_code = each
            flag = False
        else:
            check_code = check_code ^ each
    return check_code


def is_subpackage(val):
    """

    :param val: a tuple
    :return: a decimal digit!
    """
    temp = val[0]
    if temp & 64:
        return True
    else:
        return False


def is_encryption(val):
    """
    checking the 10bit if it's fill '1' mean use RSA encrytion
    return True else return False
    :return: BOOL
    """
    temp = val[0]
    if temp & 1024:
        return True  # RSA encryption!
    else:
        return False


def is_complete(val, std):
    """
    if the client crc equal the calculate value
    and then return True else return False!
    :param val: A list data, which you should calculate the crc !
    :param std: The crc code from client given!
    :return:
    """
    result = check(val)
    if result == std:
        return True  # The crc encryption equal the client send!
    else:
        return False
