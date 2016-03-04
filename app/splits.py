from hokey.convert import SplitConvertBase


class SampleSplitConvertBase(SplitConvertBase):
    """
    Input: a tuple with digit item,Example: (1,2,3,4,5,6,7,8,9,0)
    Output: a dict with the name you give `sub_split_rule`
            the type will convert to your asking,Example `to_double`
    """
    sub_split_rule = ['bar/1 | to_word', 'foo/is_true(bar)?1~3:1~5 | to_dword', 'sap/#bar | to_double',
                      'time/1 | to_time']


class PositionSplit(SplitConvertBase):
    # Required override the parent attribute
    sub_split_rule = ['alarm/4', 'status/4', 'latitude/4',
                      'longitude/4', 'altitude/2', 'speed/2',
                      'direction/2', 'timestamp/6']


if __name__ == '__main__':
    pass
