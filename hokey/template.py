import tongue
from _tools import check
from helpers import dns, pattern
from auth import simple_auth

AUTH_CODE = simple_auth()

SYSTEM_CMD = pattern(
        ('sys_ok', (0,)),
        ('sys_err', (2, 0)),
        ('sys_crc', (1,)),
        ('sys_auth', AUTH_CODE),
        ('sys_product', (0, 1)),
        ('sys_fixed_msg_attr', (0, 5)),  # This is a fixed value ,you should calculate the msg attr yourself!
        ('sys_fixed_msg_attr2', (0, 0))  # Empty message content for check terminal setting
)

"""
change the MSG_ID_ORIGINAL Dicts key
example1: 0x0100 --> (1,0)
example2: 0100 --> (1,2)
"""

AUTH_CODE = simple_auth()


def pop_each_field(small_tuple, big_tuple):
    if isinstance(small_tuple, tuple):
        for k in small_tuple:
            big_tuple.append(k)


def render(request, ruler):
    """

    :param ruler:
    :type request: object
    """
    system_cmd = SYSTEM_CMD
    temp = []
    fill_field = ruler.split("|")
    # Auto loader the old CRC for value for occupying
    fill_field.append('sys_crc')
    #: loader the data format by ruler
    for item in fill_field:
        #: if the key in the request ,and go get it!
        if item in request:
            #: because , the value will be a  tuple!
            pop_each_field(request[item], temp)

        elif item in system_cmd:
            pop_each_field(system_cmd[item], temp)

        elif item.startswith('0x'):
            cmd_tuple = dns(item)
            pop_each_field(cmd_tuple, temp)

    check_code = check(temp)
    #: change to a new CRC
    temp[-1] = check_code
    temp.insert(0, 126)
    temp.append(126)
    send_data = tuple(temp)
    if __name__ == '__main__':
        return send_data
    else:
        send_data_binary = tongue.Code(send_data).dst
    return send_data_binary


def render_ask():
    pass


def auto_render(val):
    pass


if __name__ == '__main__':
    sample = {'t_product': (1, 2), 'msg_id': (3, 5), 'sys_ok': (2,)}
    template = '0x8001|msg_id|sys_ok'
    result = render(sample, template)
    print result
