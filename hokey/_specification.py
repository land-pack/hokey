import re


def filer_wave_line(val):
    temp = val.split('~')
    result = [int(x) for x in temp]
    return result


def build_dict(val):
    """
    :param val: It's a string with some ruler Example: 'foo/is_true(bar)1~2?1~4'
    :return: {'field':'foo','fun':'is_true','arg':'bar','optA':'1~2','optB':'1~4'}
    """
    if not isinstance(val, str):
        raise ValueError("""Expect a string as param\nExample:'foo/is_true(bar)?1~3:1~5 | to_dword'""")

    val = val.replace(' ', '')
    if '|' in val:
        pattern = re.compile(r'(?P<rest>.*)\|(?P<convert_fun>.*)')
    n = pattern.match(val)
    temp_dict = n.groupdict()  # Only for get the convert_function name
    val = temp_dict['rest']
    if '?' in val:  # If you split_list have something like this Example# 'tie/is_okay(dev_id)?1~2:2~4'
        pattern = re.compile(r'(?P<field>.*)/(?P<fun>.*)\((?P<arg>.*)\)\?(?P<optA>.*):(?P<optB>.*)')
    else:
        if ':' in val:  # If you split_list have something like this Example# 'tie/1~2:1~4'
            pattern = re.compile(r'(?P<field>.*)/(?P<optA>.*):(?P<optB>.*)')
        else:  # If you split_list have something like this Example# 'tie/1'
            if '#' in val:
                # If your split_list have Example# 'foo/#bar'
                # Mean you should according the 'bar' value define foo field length .
                pattern = re.compile(r'(?P<field>.*)/#(?P<pre_field>.*)')
            else:
                # It's simple define a value for the field. Example like:'foo/3'
                pattern = re.compile(r'(?P<field>.*)/(?P<optA>.*)')

    m = pattern.match(val)
    result = m.groupdict()
    result['convert_fun'] = temp_dict['convert_fun']
    return result


def rebuild_dict(val):
    """
    :param val: It's a dict type Example : {'optA':1~3,'optB':1~5}
    :return: {'fun': 'is_true', 'field': 'foo', 'arg': 'bar', 'optA': [1, 3], 'optB': [1, 5]}
    """
    if 'optA' in val:
        if '~' in val['optA']:
            val['optA'] = filer_wave_line(val['optA'])
        else:
            val['optA'] = int(val['optA'])
    if 'optB' in val:
        if '~' in val['optB']:
            val['optB'] = filer_wave_line(val['optB'])
        else:
            val['optB'] = int(val['optB'])
    return val


def split_ruler(val):
    temp = build_dict(val)
    result = rebuild_dict(temp)
    return result
