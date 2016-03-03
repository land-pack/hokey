from hokey import rely_base


@rely_base.register_rely_func('is_okay')
def is_true_fun(val):
    """

    :param val: a tuple (1,2,3,4)
    :return: Boolean, sometime you need to test some bit ,before you decide next field length
    """
    pass


if __name__ == '__main__':
    print rely_base.rely_on_functions
