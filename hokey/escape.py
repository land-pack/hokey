from helpers import dns


class EscapeBase:
    """
    Some string have duplicate mean, so we need to escape it!
    Like 128,127 ;in fact it's mean 127! so we to escape those string!
    Now,we have the EscapeBase, you just need to told me which guys need
    to escape! you just put it override the escape_ruler at your subclass
    of EscapeBase! and the syntax like '128,127==127#128,129==129#...'
    """
    escape_ruler = ''
    singleton_flag = False

    def __init__(self, data):
        """
        :param data: a tuple
        :return: Nothing, but convert the tuple to a string!
        """
        if isinstance(data, tuple):
            self.data = str(data)
        else:
            raise TypeError('Your data is no a tuple!')

        if '0x' in self.escape_ruler:
            self.clean_escape_ruler()

        self.reverse_ruler, self.forward_ruler = self.escape_dict(self.escape_ruler)

    def clean_escape_ruler(self):
        """
        This function should called only once, so there is singleton pattern!

        To make the client configure file more easy to use
        So, in this function, we will convert something like
        ''0x7e7b==0x7e#0x7b7b==0x7b' to '126,123==123#123,123==123'
        :return:
        """
        if self.singleton_flag:
            items = self.escape_ruler.split('#')
            new_escape_str = ''
            for item in items:
                key, value = item.split('==')
                new_key = str(dns(key))
                new_value = str(dns(value))
                new_key_x = new_key.replace('(', '').replace(')', '').rstrip(',')
                new_value_x = new_value.replace('(', '').replace(')', '').rstrip(',')
                new_escape_str += new_key_x + '==' + new_value_x + '#'
            self.escape_ruler = new_escape_str.rstrip('#')
        else:
            return 'You see this!! because this function is use Singleton Pattern! Only call for one time!'

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
    # escape_ruler = '0x7e7b==0x7e#0x7b7b==0x7b'


if __name__ == '__main__':
    sample = (128, 127, 126, 123, 129, 126, 123, 128, 126)
    instance = EscapeSample(sample)
    print instance.forward()
    print instance.reverse()
    print instance.clean_escape_ruler()
