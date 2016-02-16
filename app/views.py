from hokey import Hokey
import datetime
import time

app = Hokey(__name__)


@app.route('0x8100')
def hello(request):
    print 'hello', request


@app.route('0x1010')
def my_time(request):
    return str(time.time()) + ' from: ' + request


@app.route('0x1020')
def my_today(request):
    return str(datetime.datetime.today()) + ' from: ' + request


if __name__ == '__main__':
    app.run()
