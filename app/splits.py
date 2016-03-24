from hokey import SplitConvertBase


class SampleSplitConvertBase(SplitConvertBase):
    """
    Input: a tuple with digit item,Example: (1,2,3,4,5,6,7,8,9,0)
    Output: a dict with the name you give `sub_split_rule`
            the type will convert to your asking,Example `to_double`
    """
    crc_check = False
    sub_split_rule = ['head/1', 'message_id/2', 'message_attr/2', 'device/6 | to_bcd',
                      'product/2 ', 'content/2', 'crc/1', 'tail/1']

    sub_split_rule = ['head/1', 'message_id/2', 'message_attr/2',
                      'device_id/6', 'message_product/2',
                      'package_item/is_sub(message_attr)?13~15:13~13',
                      'content/is_sub(message_attr)?15~-1:13~-1',
                      'crc/1'
                      ]


class PositionSplit(SplitConvertBase):
    # Required override the parent attribute
    crc_check = False
    sub_split_rule = ['alarm/4 | to_dword', 'status/4', 'latitude/4|to_dword',
                      'longitude/4| to_dword', 'altitude/2', 'speed/2',
                      'direction/2', 'timestamp/6| to_time']


if __name__ == '__main__':
    sample = (126, 1, 0, 0, 2, 1, 80, 51, 80, 68, 118, 0, 1, 51, 52, 5, 126)
    instance = SampleSplitConvertBase(sample)
    print instance.result
