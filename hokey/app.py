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

    #: Example below!
    #: {    "12345":{"device_id":"12345","cmd":"0x8104"}
    #:      "67890":{"device_id":"67890","cmd":"0x8107"}
    #:      "sample":{"device_id":"sample","cmd":"0x8109"} }
    current_client_requests = {}

    #: {"12345":{"server":
    current_client_response = {}

    #: A extends Dict! have a `from_object` method ,can load the configure easily!
    config = Config()

    def __init__(self, debug=True, is_binary=False):

        #: Global variable for Communicate to each function!
        self.response = ''

        self.set_socket_map = {}
        self.terminal_request_dict = {}
        self.client_request = ''
        self.client_response = ''
        #: For map the device_id to the socket ...
        self.device_id = ''
        self.is_binary_data = is_binary
        self.debug = debug

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
            new_rule = name_as_tuple(rule)  # TODO fiexed ...
            # To make '0x8100' to '(129, 1)'
            # self.view_functions[new_rule] = function_name
            self.view_functions[new_rule] = function_name

            def __route(function_arg):
                function_name(function_arg)

            return __route

        return _route

    def load_config(self):
        MainSplit.sub_split_rule = self.config.get('MAIN_SPLIT')
        MainSplit.CRC_AT = self.config.get('CRC_AT')

    def get_data(self, data):
        """
        :param data: from grasshopper
        :return: to the grasshopper
        """
        self.load_config()
        #: Call the pre_process!

        self.pre_process(data)
        #: the response will be set after process!
        return self.response

    def pre_process(self, data):
        if '{' in data and '}' in data:

            #: If the input data has '{' key, mean it's from client No terminal!
            client_request_dict = json.loads(data)

            message_id = client_request_dict['command']
            device_id = client_request_dict['device']
            #: current device should return something to client!
            self.current_client_requests[device_id] = message_id
            temp = self.current_client_requests
            self.response = str(temp)
            #: Empty all!
            self.current_client_response = {}

        else:

            #: else, we may got the binary data from terminal!
            #: so, we need to convert it to the human understand type!
            tuple_data = tongue.Decode(data).dst

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

    def dispatch_terminal_request(self):
        """Does the request dispatching. Matches the URL and returns the
        value of the view or error handler. This does not have to be a
        response object. In order to convert the return value to a proper
        response object, call:func:`make_response`
        """
        #: The message_id_key from client config instance!
        val = self.terminal_request_dict
        message_id = val[self.config.get('MESSAGE_ID', 'message_id')]

        #: The device_id_key also from client config
        device_id = val[self.config.get('DEVICE_ID', 'device_id')]

        #: update the dict for latest
        # self.latest_terminal_request[self.device_id] = self.terminal_request_dict
        #: self.device_id Example:'665','666'
        message_id = str(message_id)
        device_id = str(device_id)

        self.process_terminal_request(message_id, device_id)

    def process_terminal_request(self, message_id, device_id):
        if device_id in self.current_client_requests:
            #: If you come here, mean you should replace the 'terminal-old' message id to a new!
            #: Example old --> 0x0200    // terminal upload the position information!
            #: Example new --> 0x8104   // get the terminal information
            new_message_id = self.current_client_requests.get(device_id)

            self.make_response_to_terminal(new_message_id)
            #: pop off the client request! after the response have done!
            del self.current_client_requests[device_id]

            #: Init the a Dict with a terminal device id as it's key!
            self.current_client_response[device_id] = ''
        else:
            self.make_response_to_terminal(message_id)

    def make_response_to_terminal(self, message_id):

        if message_id in self.view_functions:
            self.response = self.view_functions[message_id](self.terminal_request_dict)
        else:
            self.response = "Can not process your data"

        if isinstance(self, str):
            if '{' in self.response and '}' in self.response:
                device = self.config.get('DEVICE_ID', 'device_id')
                key = self.response[device]
                if key in self.current_client_response:
                    self.current_client_response[key] = self.response
                    #: and then should return something to reset the terminal!!
                    #: for do that, you just return nothing !
