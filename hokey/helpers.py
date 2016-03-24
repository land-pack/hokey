import struct
import binascii
from ast import literal_eval


def url_for(func):
    pass


def dns(val):
    """
    This function work for resolve the user conf to something system
    understand syntax ! example: '0x8100' -> '(128,1)'
    :param val:
    :return:
    """
    val = val.replace('0x', '')
    val = binascii.unhexlify(val)
    data_len = len(val)
    s = struct.Struct('%iB' % data_len)
    temp_dec_k = s.unpack(val)
    # temp_hex_k = dec2hex(temp_dec_k)
    return temp_dec_k


"""
Reset a Dict your give
and change it key example below:
'8100' --> (129,1)
"""


def dns_key(val):
    """
    :param val: a Dicts type
    :return: return a new Dict with new key like a (tuple)
    """
    temp = {}
    for item in val:
        key = str(dns(item))
        temp[key] = val[item]

    return temp


def dns_value(val):
    temp = {}
    for item in val:
        temp[item] = str(dns(val[item]))
    return temp


def dns_k2v(val):
    result = {}
    temp = {value: key for key, value in val.items()}
    for item in temp:
        result[item] = literal_eval(temp[item])
    return result


def pattern(*val):
    """
    To make a tuple being a Dicts!
    :param val: a tuple-inline a tuple from the apps-urls.py
    :return: a Dicts
    """
    temp = {}
    for item in val:
        temp[item[0]] = item[1]
    return temp