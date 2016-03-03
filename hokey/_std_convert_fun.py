from convert import ConvertBase


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
