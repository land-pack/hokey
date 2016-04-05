import sys

sys.path.append("..")

from hokey import Hokey, render, redirect, url_for, auto_render
from config import Config
from splits import PositionSplit

# from models import PositionTable
# from app.models import session
# from app.models import Base, engine
# from splits import PositionSplit
#
# Base.metadata.create_all(engine)
#

app = Hokey()
app.config.from_object(Config)


## from grasshopper import GrasshopperEngine as GE
## engine = GE()
## engine.install(app)


#: 8-5 Terminal register
@app.route('0x0100')
def register(terminal_request):
    """
    :param terminal_request: original data format to Dicts from terminal!
    :return: a render which a tuple factory
    you should know what you are doing and which field you need!
    """
    template = 'message_id|message_attr|device_id|message_product|content'
    return render(terminal_request, template)


#: 8-7 Terminal unregister
@app.route('0x0003')
def unregister(terminal_request):
    pass


#: 8-8 Terminal authentication
@app.route('0x0102')
def auth(terminal_request):
    msg_content = 'message_product|message_id|sys_ok'
    template = '0x8001|sys_fixed_msg_attr|device_id|sys_product|' + msg_content
    # template = '0x8001|auto_message_attr|device_id|auto_product|'
    return render(terminal_request, template)


#: 8-12 Query terminal argument response
@app.route('0x0104')
def get_ter_info(terminal_request):
    template = 'get_ter_info|sys_fixed_msg_attr2|client_dev_id|sys_product|'
    print 'terminal_request', terminal_request
    return render(terminal_request, template)


#: 8-15 Query terminal attribute response
@app.route('0x0107')
def get_ter_attr(terminal_request):
    msg_content = ''  # Empty message content for checking terminal attribute
    template = 'get_ter_attr|sys_fixed_msg_attr2|client_dev_id|sys_product|'
    if 'GET' in terminal_request:
        # return SplitInstance.result ...
        return redirect(url_for('0x0200'), )
    return render(terminal_request, template)


#: 8-17 Terminal update result notification
@app.route('0x0108')
def update_pkg_res(val):
    pass


#: 8-18 Position report
@app.route('0x0200')
def position(terminal_request):
    # Load the field which your need to save!
    content = terminal_request['content']
    # Do some Resolution according your need!
    position_instance = PositionSplit(content)
    # Get the attribute of the PositionSplit and you'll got a Dict type
    position_info = position_instance.result
    print 'position_info', position_info
    # ORM
    # p_i = PositionTable(**position_info)
    # session.add(p_i)
    # session.commit()
    return "ok"


#: 8-20 Position query response
@app.route('0x0201')
def pos_query_rsp(val):
    pass


#: 8-25 Event report
@app.route('0x0301')
def event_report(val):
    pass


#: 8-27 Response to asked
@app.route('0x0302')
def rsp_to_ask(val):
    pass


#: 8-29 Message book/cancel
@app.route('0x0303')
def msg_book_cancel(val):
    pass


#: 8-33 Car controller response
@app.route('0x0500')
def car_c_rsp(val):
    pass


#: 8-44 Runtime log upload
@app.route('0x0700')
def run_log_upload(val):
    pass


@app.route('0x8001')
def server_common_response(client_request):
    pass


@app.route('0x8104')
def get_terminal_infor(terminal_request):
    return auto_render(terminal_request)


if __name__ == '__main__':
    ##engine.run()
    print app.view_functions
