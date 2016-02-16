import struct
import binascii
from ast import literal_eval


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


if __name__ == '__main__':
    input_sample1 = '0x8100'
    output_sample1 = name_as_tuple(input_sample1)
    print output_sample1
    print type(output_sample1)
