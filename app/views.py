import sys

sys.path.append('..')
from hokey import Hokey
from hokey import request

app = Hokey(__name__)


@app.route('0x0100')
def hello(request):
    print 'hello', request


if __name__ == '__main__':
    app.view_functions['0x0100']('ak....')
