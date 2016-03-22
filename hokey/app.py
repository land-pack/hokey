import tongue
from convert import SplitConvertBase
from _tools import name_as_tuple
import json
from ._config import Config


class MainSplit(SplitConvertBase):
    crc_check = True
    CRC_AT = -2
    sub_split_rule = []


class Base:
    #: A dictionary of all view functions registered.  The keys will
    #: be function names which are also used to generate MESSAGE_IDs and
    #: the values are the function objects themselves.
    #: To register a view function, use the :meth:`route` decorator.
    view_functions = {}

    #: Store the latest terminal request for client use!
    latest_terminal_request = {}
    #: {"123":{"client":"GET","device":"123","cmd":"0x8100"},{"456":{"client":"SET"..}}
    current_client_requests = {}
    done_client_request = {}
    #: A extends Dict! have a `from_object` method ,can load the configure easily!
    config = Config()

    def __init__(self):

        #: The original data from terminal/client will fill here!
        self.data = ''

        #: Global variable for Communicate to each function!
        self.response = ''

        self.prefix = self.config.get('PREFIX')
        MainSplit.sub_split_rule = self.config.get('MAIN_SPLIT')

        #: The latest terminal request will put here!
        self.terminal_request_dict = {}

        #: The latest client request will put here!
        self.client_request_dict = {}

    def input(self, data):
        """
        :param data: from grasshopper
        :return: to the grasshopper
        """
        self.data = data
        #: Call the pre_process!
        self.pre_process()

        #: the response will be set after process!
        return self.response

    def pre_process(self):
        if 'client' in self.data:

            #: If the input data has 'client' key, mean it's from client No terminal!
            self.client_request_dict = json.loads(self.data)

            #: So we will call the client dispatch!
            self.dispatch_client_request()
        else:

            #: else, we may got the binary data from terminal!
            #: so, we need to convert it to the human understand type!
            tuple_data = tongue.Decode(self.data).dst

            #: we will (126, 1, 2, 0, 2, 1, 80, 51, 80, 68, 118, 0, 3, 51, 52, 5, 126)
            request_context = MainSplit(tuple_data)

            #: After MainSplit process, we got a split instance!
            self.terminal_request_dict = request_context.result

            #: The below dict, is we got for now, we can easy to checking each field with the name!
            #: {'device': '15033504476', 'content': (51, 52), 'product': 1, 'message_id': (1, 0), 'message_attr': 2}
            #: Now, we have fill-full our terminal_request_dict!
            self.dispatch_terminal_request()

    def dispatch_client_request(self):
        """
        This method will override on the sub-class! `Hokey`
        :return:
        """
        pass

    def dispatch_terminal_request(self):
        """
        This method will override on the sub-class `Hokey`
        :return:
        """
        pass


class Hokey(Base):
    """
    This class work for map the message id to the view functions
    also work for checking receive data ...
    """

    def __init__(self, is_binary_data_recv=True):
        self.set_socket_map = {}
        self.response = ''

        self.client_request = ''
        self.client_response = ''
        #: For map the device_id to the socket ...
        self.device_id = ''
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
        #: The message_id_key from client config instance!
        message_id = self.terminal_request_dict[self.config.get('MESSAGE_ID', 'message_id')]

        #: The device_id_key also from client config
        self.device_id = self.terminal_request_dict[self.config.get('DEVICE_ID', 'device_id')]

        #: update the dict for latest
        self.latest_terminal_request[self.device_id] = self.terminal_request_dict
        #: self.device_id Example:'665','666'

        if self.device_id in self.done_client_request:
            self.client_response[self.device_id] = self.terminal_request_dict
            del self.current_client_requests[self.device_id]
            del self.done_client_request[self.device_id]
        else:
            if self.device_id in self.current_client_requests:
                # This request should response to the client no the terminal!
                command = self.view_functions[self.device_id]['command']  # command == message_id

                if message_id in self.view_functions:
                    self.client_response = self.view_functions[command](self.terminal_request_dict)
                    # Redirect ....to a new view functions ...by 'command'
                    self.done_client_request[self.device_id] = 'done'
                    del self.current_client_requests[self.device_id]  # Okay the current client request have process!
                else:
                    self.client_response = "Can't not process your data"
            else:
                self.make_response_to_terminal(message_id)

    def make_response_to_terminal(self, message_id):
        if message_id in self.views_functions:
            self.response = self.views_functions[message_id](self.terminal_request_dict)
        else:
            self.response = "Can not process your data"

    def dispatch_client_request(self):
        """
        Input a dict as it's param, according th
        e Dict-Key and do next step!
        :return:
        """
        message_id = self.client_request_dict['command']
        device_id = self.client_request_dict['device']

        self.current_client_requests[device_id] = message_id  # current device should return something to client!

    def set_key(self):
        """
        By resolution the data,and get the device_id out.
        will return the device_id as the socket_map key!!
        """
        if self.is_client_data():
            return "xxx"
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
