from hokey.convert import SplitConvertBase
from views import app


@app.required_split
class MainSplit(SplitConvertBase):
    # override the parent attribute
    prefix = 'client_'
    crc_check = True
    split_list = ['head_tag/1', 'msg_id/2', 'msg_attr/2',
                  'dev_id/6', 'msg_product/2',
                  'package_item/is_subpackage(msg_attr)?13~15:13~13',
                  'content/is_subpackage(msg_attr)?15~-2:13~-2',
                  'crc/-2~-1'
                  ]


class SampleSplitConvertBase(SplitConvertBase):
    """
    Input: a tuple with digit item,Example: (1,2,3,4,5,6,7,8,9,0)
    Output: a dict with the name you give `sub_split_rule`
            the type will convert to your asking,Example `to_double`
    """
    sub_split_rule = ['bar/1 | to_word', 'foo/is_true(bar)?1~3:1~5 | to_dword', 'sap/#bar | to_double',
                      'time/1 | to_time']


if __name__ == '__main__':
    pass
