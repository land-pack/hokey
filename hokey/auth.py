import random

NUM_OF_CODE = 8

def simple_auth():
    result_list = []
    for i in range(NUM_OF_CODE):
        temp = random.randint(1, 100)
        result_list.append(temp)
    return tuple(result_list)
