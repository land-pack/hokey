from split import SplitBase


class MainSplit(SplitBase):
    # override the parent attribute
    prefix = 'client_'
    crc_check = True
    split_list = ['head_tag/1', 'msg_id/2', 'msg_attr/2',
                  'dev_id/6', 'msg_product/2',
                  'package_item/is_subpackage(msg_attr)?13~15:13~13',
                  'content/is_subpackage(msg_attr)?15~-2:13~-2',
                  'crc/-2~-1'
                  ]
