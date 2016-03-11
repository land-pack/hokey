from app import create_app
from hokey import render
from settings import DevelopmentConfig

from models import PositionTable
from app.models import session
from app.models import Base, engine

Base.metadata.create_all(engine)

from splits import PositionSplit

# from grasshopper import GrasshopperEngine as GE
app = create_app(config_name=DevelopmentConfig)


@app.route('0x0100', '0x8100')
def register(terminal_request):
    """
    :param terminal_request: original data format to Dicts from terminal!
    :return: a render which a tuple factory
    you should know what you are doing and which field you need!
    """
    template = 'client_msg_id|client_msg_attr|client_dev_id|client_msg_product|client_content'
    return render(terminal_request, template)


@app.route('0x0102')
def auth(terminal_request):
    msg_content = 'client_msg_product|client_msg_id|sys_ok'
    template = '0x8001|sys_fixed_msg_attr|client_dev_id|sys_product|' + msg_content
    print 'terminal_request', terminal_request
    return render(terminal_request, template)


@app.route('0x0200')
def position(terminal_request):
    # Load the field which your need to save!
    content = terminal_request['client_content']
    # Do some Resolution according your need!
    position_instance = PositionSplit(content)
    # Get the attribute of the PositionSplit and you'll got a Dict type
    position_info = position_instance.result
    print 'position_info', position_info
    # ORM
    p_i = PositionTable(**position_info)
    session.add(p_i)
    session.commit()


@app.route('0x0104')
def get_ter_info(terminal_request):
    template = 'get_ter_info|sys_fixed_msg_attr2|client_dev_id|sys_product|'
    print 'terminal_request', terminal_request
    return render(terminal_request, template)


@app.route('0x0107')
def get_ter_attr(terminal_request):
    msg_content = ''  # Empty message content for checking terminal attribute
    template = 'get_ter_attr|sys_fixed_msg_attr2|client_dev_id|sys_product|'
    if 'GET' in terminal_request:
        # return SplitInstance.result ...
        pass
    return render(terminal_request, template)


def main():
    # engine = GE(host='0.0.0.0',port=5555)
    # engine.install(app)
    # engine.run()
    pass


if __name__ == '__main__':
    # main()
    pass
