from hokey.convert import SplitConvertBase


class SampleSplitConvertBase(SplitConvertBase):
    """
    Input: a tuple with digit item,Example: (1,2,3,4,5,6,7,8,9,0)
    Output: a dict with the name you give `sub_split_rule`
            the type will convert to your asking,Example `to_double`
    """
    crc_check = True
    sub_split_rule = ['message_id/2', 'message_attr/2 | to_int', 'device/6 | to_bcd',
                          'product/2 | to_int', 'content/2 | to_int']


class PositionSplit(SplitConvertBase):
    # Required override the parent attribute
    sub_split_rule = ['alarm/4 | to_dword', 'status/4', 'latitude/4',
                      'longitude/4', 'altitude/2', 'speed/2',
                      'direction/2', 'timestamp/6']


if __name__ == '__main__':
    sample = (126, 1, 0, 0, 2, 1, 80, 51, 80, 68, 118, 0, 1, 51, 52, 5, 126)
    instance = SampleSplitConvertBase(sample)
    print instance.result