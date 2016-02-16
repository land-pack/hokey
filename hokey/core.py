from tools.nickname import name_as_tuple
from swi import view_functions
from swi import main


class Hokey:
    def __init__(self, app_name):
        self.name = app_name

        #: A dictionary of all view functions register. The keys will
        #: be function names which are also used to generate URLs and
        #: the values are the function objects themselves.
        #: To register a view function, use the :meth:`route` decorator.
        # self.view_functions = {}

    def request(self, rule):
        pass

    def run(self, debug=False):
        main()

    def add_url_rule(self, ruler, endpoint=None, view_func=None, **options):
        pass

    def route(self, rule):
        """
        A decorator that is used to register a view function for a given
        URL rule. This does the same thing as :meth:`add_url_rule` but
        is intended for decorator usage::

            @app.route('0x0100')
            def index():
                pass

        Is equivalent to the following::

            def index():
                pass
            app.add_url_rule('0x0100','index',index)

        If the view_func is not provided you will need to connect the
        endpoint to a view function like so::

            app.view_functions['index'] = index

        :param	rule: the URL rule as string
        """

        def _route(function_name):
            new_rule = name_as_tuple(rule)
            # self.view_functions[new_rule] = function_name
            view_functions[new_rule] = function_name

            def __route(function_arg):
                function_name(function_arg)

            return __route

        return _route

    def dispatch_request(self):
        """Does the request dispatching. Matches the URL and returns the
        value of the view or error handler. This does not have to be a
        response object. In order to convert the return value to a proper
        response object, call:func:`make_response`
        """
        pass

    def make_response(self, rv):
        pass

    def preprocess_request(self):
        pass

    def process_response(self, response):
        pass

    def request_context(self, environ):
        pass


app = Hokey(__name__)


@app.route('0x8100')
def hello(a):
    print 'hello a', a


if __name__ == '__main__':
    app.run()
