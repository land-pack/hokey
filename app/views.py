from app import create_app
from hokey import render
import datetime
import time
from config import DevelopmentConfig

app = create_app(config_name=DevelopmentConfig)


@app.route('0x8100')
def hello(request):
    template = 'get_ter_info|sys_fixed_msg_attr2|client_dev_id|sys_product|'
    print 'terminal_request', request
    # TODO ORM here
    return render(request, template)


@app.route('0x1010')
def my_time(request):
    return str(time.time()) + ' from: ' + request


@app.route('0x1020')
def my_today(request):
    return str(datetime.datetime.today()) + ' from: ' + request


if __name__ == '__main__':
    app.run()
