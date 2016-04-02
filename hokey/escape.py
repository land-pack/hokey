class EscapeBase:
    """
    Some string have duplicate mean, so we need to escape it!
    Like 128,127 ;in fact it's mean 127! so we to escape those string!
    Now,we have the EscapeBase, you just need to told me which guys need
    to escape! you just put it override the escape_ruler at your subclass
    of EscapeBase! and the syntax like '128,127==127#128,129==129#...'
    """
    escape_ruler = ''

    def __init__(self, data):
        """
        :param data: a tuple
        :return: Nothing, but convert the tuple to a string!
        """
        self.data = str(data)
        self.reverse_ruler, self.forward_ruler = self.escape_dict(self.escape_ruler)

    def escape_dict(self, esc_str):
        """
        param `esc_str` Just a simple ruler
        this function will return a tuple, which take two dict!
        For input example: '128,127==127# 128, 129==129'
        """

        dict_a = {}
        dict_b = {}
        del_space = esc_str.replace(' ', '')
        escape_list = del_space.split('#')
        for i in escape_list:
            key, value = i.split("==")
            dict_a[key] = value
            dict_b[value] = key
        return dict_b, dict_a

    def escape(self, dst, escape_table):
        """
            This function for escape some string !
            param `dst`: is a string , we should do some escape !
            param `escape_table` is a python Dicts, we should read it !
            For example: '128,127' --> '127'
        """

        dst = dst.replace(' ', '')
        for k in escape_table:
            if k in dst:
                dst = dst.replace(k, escape_table[k])
        return dst

    def forward(self):
        return eval(self.escape(self.data, self.forward_ruler))

    def reverse(self):
        return eval(self.escape(self.data, self.reverse_ruler))


class EscapeSample(EscapeBase):
    """
    You can override your escape_ruler on your subclass!
    """
    escape_ruler = '128,127==127#128,129==129'


if __name__ == '__main__':
    sample = (128, 127, 127, 128, 129, 122, 1, 128, 126)
    instance = EscapeSample(sample)
    print instance.forward()
    print instance.reverse()
