class App:
    views_functions = {}
    counter = 0

    def __init__(self):
        self.data = ''

    def process_request(self, val):
        self.data = val  # Get the data from ...grasshopper..
        print '*' * 50
        print 'processing....'
        if 'foo' in val:
            self.views_functions['bar'](val)
        elif 'bar' in val:
            self.views_functions['foo'](val)
        else:
            print 'Can process your data..'
        return 'done...\n'

    def set_key(self):
        """
        By resolution the data,and get the device_id out.
        will return the device_id as the socket_map key!!
        """
        self.counter += 1
        return 'xx' + str(self.counter)

    def route(self, rule):
        def _route(fun):
            self.views_functions[rule] = fun

            def __route(fun_arg):
                fun(fun_arg)

            return __route

        return _route
