from collections import OrderedDict


def render(requests, ruler):
    pass


if __name__ == '__main__':
    sample_requests = 'message_id|message_attr|device_id|message_product|content'
    sample_ruler = {'message_id': (1, 2),'message_attr': (2, 3), 'device_id': (1, 2, 3, 4, 5, 6),
                    'message_product': (0, 1), 'content': (1, 2, 3, 4, 5, 6, 7, 8, 9)}

    placeholder = sample_requests.split('|')
    for i in placeholder:
        print i
