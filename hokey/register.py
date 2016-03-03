from . import convert_base


@convert_base.register_convert_func('is_true')
def is_true_guy(val):
    print 'yes, it is true'


if __name__ == '__main__':
    print convert_base.convert_functions
