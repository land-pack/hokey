from hokey import ConvertBase  # system instance of ConvertBase


@ConvertBase.register_convert_func('is_true')
def is_true(val):
    print 'yes , it is true'


if __name__ == '__main__':
    print ConvertBase.convert_functions
