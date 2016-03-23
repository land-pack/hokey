from _re_pattern import split_ruler
from _tools import is_complete


class ConvertBase:
    convert_functions = {}

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

    #: A list for the regular express process!
    #: And this class attribute should always be override by the client!
    #: Example override it like the below!
    #: sub_split_rule = ['message_id/2', 'message_attr/2 | to_int', 'device/6 | to_bcd',
    #:                      'product/2 | to_int', 'content/2 | to_int']
    sub_split_rule = []

    #: Work like the view_functions!
    dependent_functions = {}

    #: The result is Dict store the data which process by the SplitConvertBase
    #: It's should be clear and human understand type with some name !
    #: Example your have some data:
    #:
    #: {'device': '15033504476', 'content': 13108, 'product': 1, 'message_id': (1, 0), 'message_attr': 2}
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
    #: Sometime, you just ignore the CRC checking,
    crc_check = False
    CRC_AT = -2

    def __init__(self, val):
        self.convert_fun = None
        self.dependent_fun = None
        """
        :param val: A tuple Example (126, 1, 0, 0, 2, 1, 80, 51, 80, 68, 118, 0, 1, 51, 52, 5, 126)
        :return: A SplitConvertBase-Subclass instance!
        """
        self.debug = True
        #: The result of the SplitBase
        self.result = {}

        #: if the subclass no override it, raise a valueError exception!
        if not self.sub_split_rule:
            print 'Sub_split_rule-->', self.sub_split_rule
            raise ValueError("The sub_split_rule can't empty!")
        if val:

            if self.crc_check:
                self.message_head_content = val[1:-1]

                #: You should tell the hokey on the configure class
                #: And where is the crc place, default CRC_AT --> -2
                self.crc = val[self.CRC_AT]
                if is_complete(self.message_head_content, self.crc):
                    self.build_dict(self.message_head_content)
                else:
                    #: ignore this request from terminal device
                    self.debug = False
                    raise TypeError('No complete data from client!')
            else:
                self.build_dict(val)
        else:
            raise ValueError('No validation input!')

    def build_dict(self, val):
        """
        :param val: (1,2,3,4,5,6,7,8,9)
        :return: None
        """
        #: You will cut the tuple step by step
        #: so you should have a base_index to know which step you have come
        #: Decide where is next cut point!
        base_index = 0

        #: It's easy to understand,it's just a variable store the current tuple
        #: length, and then decide how many step we can cut the all data `val`
        split_list_length = len(self.sub_split_rule)

        #: Here we put the sub_list_rule each time/step
        #: Example,we have ['message_id/2', 'message_attr/2 | to_int', 'device/6 | to_bcd']
        #: for the first loop, we get the 'message_id/2' out
        for index in range(split_list_length):

            #: split_rule is very power regular express function,
            #: In fact, you can call micro template language!
            spd = split_ruler(self.sub_split_rule[index])

            #: the fill_field just a name you given where you define your `sub_split_rule`
            #: Example  -->['message_id/2', 'message_attr/2 | to_int', 'device/6 | to_bcd']
            #: You fill_field will be 'message_id' and 'message_attr' ,etc ...
            fill_field = spd['field']

            #: Sometime, We don't need to covert the type, so we should define a flag
            #: Here, we just initial the flag!
            whether_convert = False
            if 'convert_fun' in spd:
                #: If we have the convert_fun ,mean we should convert it on the next!
                whether_convert = True

                #: Here, we get the convert_fun name!
                #: it's we work for us on the next step!
                convert_fun_name = spd['convert_fun']  # Will get the name of convert function. Example: `to_word`

                #: Here, we get the real convert function object by check our convert_function Dicts!
                convert_fun = self.convert_functions[convert_fun_name]  # Will get the object of convert function

            #: Sometime, we also need some to check some field, before we decide how length the next field !
            #: so we should have a fun to do it! may be just checking the value, maybe just checking the bit!
            if 'fun' in spd:

                #: Here, we get the dependent_functions name!
                #: Example: `is_true`
                dependent_fun_name = spd['fun']

                #: Get the real dependent_functions object!
                dependent_fun = self.dependent_functions[dependent_fun_name]

                #: A function must take some argument, so we should get the argument name
                #: Usually,it's should be the pre-field name we got!!
                #: Example, We have the data --> ['message_attr/2','device/length(message_attr) | to_bcd']
                #: The dependent fun is `length` and the argument is `message_attr`
                # func_arg_field = self.prefix + spd['arg']
                func_arg_field = spd['arg']
                #: If you get the argument name, and then you can check the result dict!
                #: Where we have store our process result place!
                #: Which field you need to checking of the result!
                func_arg = self.result[func_arg_field]

                #: And then you got the value by the `length` return --> 2
                if dependent_fun(func_arg):

                    #: if you return True ,pick the optA as it's field_range
                    #: Example --> ['foo/1,'bar/is_true(foo)?12:34'], ---> pick optA --> 12
                    field_range = spd['optA']
                else:
                    #: else pick optB --> 34
                    field_range = spd['optB']
                    # ---------------------------------------------------------------

            else:
                #: Mean this field size dependent on the pre field value!!
                if 'pre_field' in spd:

                    #: Example: ['foo/1','bar/#foo']
                    pre_field_name = spd['pre_field']

                    #: and the pre_field_name will be 'foo' and it's only take `1Bit`
                    #: so we assume it's value '23'
                    #: if the foo is '23', the ruler should be 'bar/23'
                    pre_field_value = self.result[pre_field_name]

                    #: get the element from list , val[23:] ---> 23
                    spd['optA'] = pre_field_value[0]
                    field_range = spd['optA']
                else:
                    #: Example --> ['foo/1','bar/#foo'], will get the 1 directly
                    field_range = spd['optA']
                    # ---------------------------------------------------------------

            #: The field_range can be 23, also can be a list [1,3]
            if isinstance(field_range, list):
                #: Example [1,3] , begin --> 1
                begin = field_range[0]
                #: end --> 3
                end = field_range[1]
                #: According the begin & end ,cut the tuple,Example,val=(1,2,3,4)
                #: The field_value will be field_value --> (2,3,4)
                field_value = val[begin:end]

                #: The length of the split, it's will add to the base_index
                #: Just for remember how many step you have cut!
                split_range = len(field_value)
            else:
                #: The field_range here we got a integer !
                #: so ,we simple cut the tuple `val` by the point ,No the range!
                split_range = base_index + field_range
                field_value = val[base_index:split_range]

            #: increase the index,move to next field,..
            base_index = split_range

            #: At the end, you should check the flag ! and then decide whether convert the data!
            #: convert the field value to your need by call the convert function from convert_function
            if whether_convert:
                if len(field_value) > 2:
                    field_value_custom_type = convert_fun(field_value)
                else:
                    raise ValueError("Your data is not complete! can't convert it!")
            else:
                field_value_custom_type = field_value
            self.result[fill_field] = field_value_custom_type
