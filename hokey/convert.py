from _re_pattern import split_ruler
from tools import is_complete


class ConvertBase:
    convert_functions = {}

    def __init__(self):
        pass

    @classmethod
    def register_convert_func(cls, rule):
        def _route(function_name):
            cls.convert_functions[rule] = function_name

            def __route(function_arg):
                function_name(function_arg)

            return __route

        return _route


class SplitBase:
    """
    By doing @map, you can add more judge function
    we are already have `is_true` function here ...
    """
    main_split_rule = []
    sub_split_rule = []
    dependent_functions = {}  # TODO should be inside __init__() ?
    result = {}

    @classmethod
    def register_rely_func(cls, rule):
        def _route(function_name):
            cls.dependent_functions[rule] = function_name

            def __route(function_arg):
                function_name(function_arg)

            return __route

        return _route


class SplitConvertBase(SplitBase, ConvertBase):
    def __init__(self, val):
        self.convert_fun = None
        self.dependent_fun = None
        """
        :param val: a tuple (1,2,3,4,5,6,7,8)
        :return:
        """
        self.debug = True
        self.result = {}  # The result of the SplitBase
        if not self.sub_split_rule:  # if the subclass no override it, raise a valueError exception!
            raise ValueError("The sub_split_rule can't empty!")
        if val:

            if self.crc_check:
                self.message_head_content = val[1:-1]
                self.crc = val[-2]
                if is_complete(self.message_head_content, self.crc):  # TODO Fixed
                    self.build_dict(val)
                else:
                    # ignore this request from terminal device
                    self.debug = False
                    ValueError('No complete data from client!')
            else:
                self.build_dict(val)
        else:
            raise ValueError('No validation input!')

    def build_dict(self, val):
        """
        :param val: (1,2,3,4,5,6,7,8,9)
        :return: None
        """
        base_index = 0
        split_list_length = len(self.split_list)

        for index in range(split_list_length):
            spd = split_ruler(self.split_list[index])
            fill_field = self.prefix + spd['field']
            whether_convert = False
            if 'convert_fun' in spd:
                whether_convert = True
                convert_fun_name = spd['convert_fun']  # Will get the name of convert function. Example: `to_word`
                convert_fun = self.convert_functions[convert_fun_name]  # Will get the object of convert function
            # ---------------------------------------------------------------
            if 'fun' in spd:
                dependent_fun_name = spd['fun']  # Will get thr name of dependent function. Example: `is_true`
                dependent_fun = self.dependent_functions[dependent_fun_name]
                func_arg_field = self.prefix + spd['arg']
                func_arg = self.result[func_arg_field]  # Which field you need to checking of the result!
                if dependent_fun(func_arg):
                    # if you return True ,pick the optA as it's field_range
                    field_range = spd['optA']  # Example: ['foo/1,'bar/is_true(foo)?12:34'], ---> pick optA --> 12
                else:
                    field_range = spd['optB']  # ... else pick optB --> 34
            # ---------------------------------------------------------------

            else:
                if 'pre_field' in spd:  # Mean this field size dependent on the pre field value!!
                    pre_field_name = spd['pre_field']  # Example: ['foo/1','bar/#foo'] ,
                    # and the pre_field_name will be 'foo'
                    pre_field_value = self.result[pre_field_name]  # if the foo is '23', the ruler should be 'bar/23'
                    spd['optA'] = pre_field_value[0]  # get the element from list , [23] ---> 23
                    field_range = spd['optA']
                else:
                    field_range = spd['optA']  # Example: ['foo/1','bar/#foo'], will get the 1 directly
            # ---------------------------------------------------------------
            if isinstance(field_range, list):  # The field_range can be 23, also can be a list [1,3]
                begin = field_range[0]  # Example [1,3] , begin --> 1
                end = field_range[1]  # ...        , end --> 3
                field_value = val[begin:end]  # according the begin & end ,cut the tuple,Example,val=(1,2,3,4),
                # The field_value will be field_value --> (2,3,4)
                split_range = len(field_value)  # The length of the split
            else:
                split_range = base_index + field_range  # The field_range here we got a integer !
                field_value = val[base_index:split_range]
            base_index = split_range  # increase the index,move to next field,..
            # convert the field value to your need by call the convert function from convert_function
            if whether_convert:
                field_value_custom_type = convert_fun(field_value)
            else:
                field_value_custom_type = field_value
            self.result[fill_field] = field_value_custom_type


# -----------------------Testing----------------------
class SampleSplitConvertBase(SplitConvertBase):
    sub_split_rule = ['bar/1 | to_word', 'foo/is_true(bar)?1~3:1~5 | to_dword', 'sap/#bar | to_double',
                      'time/1 | to_time']


if __name__ == '__main__':
    # sample_input = (3, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19)
    # sample_instance_2 = ConvertBase()
    print ConvertBase.convert_functions
