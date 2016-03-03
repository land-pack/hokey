import tongue
from . import main_split  # Global variable
from . import is_binary_data_receiver
from . import MSG_ID


class Dispatch:
    """
    Dispatch have two very important attribute
    1> message_id   : It's decide which view_functions should be called!
    2> request      : It's Dicts type, all client data format as client splits.py
    define ,it's usually call MainSplit,
    """

    def __init__(self, receive_data):
        """
        :param receive_data: `0101001010`
        :return: A Dict type {'abc':(1,2),'def':(3,4)}
        """

        if is_binary_data_receiver:
            decimal_tuple = tongue.Decode(receive_data).dst
        else:
            decimal_tuple = receive_data
        # decimal_data: `(1,2,3,4,5,6,7)`
        if '/' in main_split:
            main_split_instance = main_split['/'](decimal_tuple)
            self.request = main_split_instance.result
            # message_id_field Example: `(2,3)` part
            self.message_id = str(self.request[MSG_ID])
            # self.message_id Example:  "(2,3)" a string as Dict key
        else:
            raise KeyError("No such key call '/'")
