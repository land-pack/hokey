import tongue
from hokey.main import MainSplit


class Dispatch:
    def __init__(self, binary_data):
        """
        :param binary_data: `0101001010`
        :return: A Dict type {'abc':(1,2),'def':(3,4)}
        """
        decimal_data = tongue.Decode(binary_data).dst
        self.request_dict = MainSplit(decimal_data).result
        self.message_id = str(self.request_dict['client_msg_id'])
