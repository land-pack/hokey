from configbase import ConfigBase
import tongue
from convert import SplitConvertBase
from tools import name_as_tuple
import json


class MainSplit(SplitConvertBase):
    sub_split_rule = []


class Hokey:
    """
    This class work for map the message id to the view functions
    also work for checking receive data ...
    """
    view_functions = {}

    def __init__(self, config_name=ConfigBase, is_binary_data_recv=True):
        self.data = ''
        self.set_socket_map = {}
        self.response = ''
        self.terminal_request_dict = {}
        self.client_request_dict = {}
        self.client_request = ''
        self.client_response = ''
        self.device_id = ''  # For map the device_id to the socket ...
        # ------------------------------------------------------------------#
        self.config_instance = config_name()  # Config instance or Config Subclass
        self.prefix = self.config_instance.PREFIX
        self.message_id_key = self.config_instance.MESSAGE_ID
        self.device_id_key = self.config_instance.DEVICE_ID
        # -------------------------------------------------------------------#
        MainSplit.sub_split_rule = self.config_instance.MAIN_SPLIT  # override the sub_split_list
        #: A dictionary of all view functions register. The keys will
        #: be function names which are also used to generate URLs and
        #: the values are the function objects themselves.
        #: To register a view function, use the :meth:`route` decorator.
        # self.view_functions = {}

        is_binary_data = is_binary_data_recv
        # If you set is_binary_data being False
        # You will deal with normally string data, no binary data
        # It's mean you will no call tongue to Decode/Code data any more

    def request(self, rule):
        pass

    def route(self, rule):
        """
        A decorator that is used to register a view function for a given
        URL rule. This does the same thing as :meth:`add_url_rule` but
        is intended for decorator usage::

            @app.route('0x0100')
            def index():
                pass

        Is equivalent to the following::

            def index():
                pass
            app.add_url_rule('0x0100','index',index)

        If the view_func is not provided you will need to connect the
        endpoint to a view function like so::

            app.view_functions['index'] = index

        :param	rule: the URL rule as string
        """

        def _route(function_name):
            # TODO
            new_rule = name_as_tuple(rule)  # TODO fiexed ...
            # To make '0x8100' to '(129, 1)'
            # self.view_functions[new_rule] = function_name
            self.view_functions[new_rule] = function_name

            def __route(function_arg):
                function_name(function_arg)

            return __route

        return _route

    def dispatch_terminal_request(self):
        """Does the request dispatching. Matches the URL and returns the
        value of the view or error handler. This does not have to be a
        response object. In order to convert the return value to a proper
        response object, call:func:`make_response`
        """
        message_id = self.terminal_request_dict[self.message_id_key]  # The message_id_key from client config instance!
        self.device_id = self.terminal_request_dict[
            self.device_id_key]  # The device_id_key also from client config class instance!
        if message_id in self.views_functions:
            self.response = self.views_functions[message_id](self.terminal_request_dict)
        else:
            self.response = "Can not process your data"

    def dispatch_client_request(self):
        """
        Input a dict as it's param, according the Dict-Key and do next step!
        :return:
        """
        message_id = self.client_request_dict['command']
        device_id = self.client_request_dict['device']

    def process_request(self, client_request):
        self.data = client_request  # Get the data from ...grasshopper..
        if self.is_client_data():  # If the message from client ...
            self.client_request_dict = json.load(self.data)
            self.dispatch_client_request()
        else:  # If the message from terminal ...
            tuple_data = tongue.Decode(self.data).dst  # (126, 1, 2, 0, 2, 1, 80, 51, 80, 68, 118, 0, 3, 51, 52, 5, 126)
            request_context = MainSplit(tuple_data)
            self.terminal_request_dict = request_context.result
            self.dispatch_terminal_request()
        return self.response

    def set_key(self):
        """
        By resolution the data,and get the device_id out.
        will return the device_id as the socket_map key!!
        """
        return self.device_id  # {'15754710000':socket_fd}

    def set_socket_map(self, val):
        self.set_socket_map = val

    def is_client_data(self):
        """
        There are should have a protocols for client!
        :return:
        """
        if 'client' in self.data:  # Client control protocol...
            return True
        else:
            return False

    def make_response(self, rv):
        """
        Make a response for the client ,if the user want to know his/her device work status!
        :param rv:
        :return:
        """

    def required_split(self, NewClass):
        """
        For register a main split class ,
        :param NewClass:
        :return:
        """
        self.example['/'] = NewClass

        class B:
            pass

        return B

    def process_response(self, response):
        pass

    def request_context(self, environ):
        pass
