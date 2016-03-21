import tongue
from _tools import check

counter = 0


def new_counter():
    global counter
    counter += 1
    return counter


def render(request, ruler):
    """

    :param ruler:
    :type request: object
    """
    system_cmd = SYSTEM_CMD
    sys_id = SYS_ID
    temp = []
    each = ruler.split("|")
    each.append('sys_crc')  # Auto loader the old CRC for value for occupying
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
