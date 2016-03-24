import tongue
from _tools import check

import struct
import binascii
from ast import literal_eval
from auth import simple_auth

AUTH_CODE = simple_auth()


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


SYSTEM_CMD = pattern(
        ('sys_ok', (0,)),
        ('sys_err', (2, 0)),
        ('sys_crc', (1,)),
        ('sys_auth', AUTH_CODE),
        ('sys_product', (0, 1)),
        ('sys_fixed_msg_attr', (0, 5)),  # This is a fixed value ,you should calculate the msg attr yourself!
        ('sys_fixed_msg_attr2', (0, 0))  # Empty message content for check terminal setting
)

MSG_ID_ORIGINAL = pattern(
        ('0x0100', 'ter_reg_req'),
        ('0x8100', 'ser_reg_rsp'),
        ('0x0102', 'ter_aut_req'),
        ('0x8001', 'ser_com_rsp'),
        ('0x0200', 'position'),
        ('0x8104', 'get_ter_info'),
        ('0x0104', 'get_ter_info_rsp'),
        ('0x8107', 'get_ter_attr'),
        ('0x0107', 'get_ter_attr_rsp')
)

"""
change the MSG_ID_ORIGINAL Dicts key
example1: 0x0100 --> (1,0)
example2: 0100 --> (1,2)
"""
MSG_ID = dns_key(MSG_ID_ORIGINAL)

SYS_ID = dns_k2v(MSG_ID)


def render(request, ruler):
    """

    :param ruler:
    :type request: object
    """
    system_cmd = SYSTEM_CMD
    sys_id = SYS_ID
    temp = []
    each = ruler.split("|")
    # Auto loader the old CRC for value for occupying
    each.append('sys_crc')
    for item in each:  # loader the data format by ruler
        if item in request:  # if the key in the request ,and go get it!
            if isinstance(request[item], tuple):  # because , the value will be a  tuple!
                for k in request[item]:  # get each element of the tuple!
                    temp.append(k)
        elif item in system_cmd:
            if isinstance(system_cmd[item], tuple):
                for k in system_cmd[item]:
                    temp.append(k)
        elif item in sys_id:
            if isinstance(sys_id[item], tuple):
                for k in sys_id[item]:
                    temp.append(k)

    check_code = check(temp)
    temp[-1] = check_code  # change to a new CRC
    temp.insert(0, 126)  # Add the header tag
    temp.append(126)  # Append the tail tag
    send_data = tuple(temp)  # For testing ..........
    send_data_binary = tongue.Code(send_data).dst
    if 'GET' in request:
        request['GET'].sendall(send_data_binary)
    else:
        print 'No Get attribute,You may run it on local main()'
    return True  # will got a tuple for response
