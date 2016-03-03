from hokey import Hokey


# from sqlalchmey import SQLAlchemy
# db = SQLAlchemy()

def create_app(config_name):
    app = Hokey(config_name, is_binary_data_recv=False)
    return app
