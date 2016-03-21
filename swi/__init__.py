# Server Gateway Interface
# The server passes all requests it receives from client to this
# object for handling, using a protocol called SGI
"""
Clients such as GPS terminal send requests to the server, which in turn sends them
to the Hokey application instance. The application instance needs to know what code
needs to run for each URI requested, so it keeps a mapping of URIs to Python functions.
The association between a URI and the function that handles it is called a route.
"""
import asyncore
import socket
from swi.dispatch import Dispatch
from hokey._config import ConfigBase

# Define Global variable here
view_functions = {}
main_split = {}
is_binary_data_receiver = False
MSG_ID = ConfigBase.MESSAGE_ID


class AnswerRequest:
    def __init__(self, request):
        """
        Recv from the client request by socket!
        and then return the response to them as soon as possible!
        param::data; a string split by '|' character!
        """
        try:
            dispatch_instance = Dispatch(request)
            URL = dispatch_instance.message_id  # Map to the function name
            if URL in view_functions:
                # call app view functions here!
                new_request = dispatch_instance.request
                self.response = view_functions[URL](new_request)
            else:
                raise KeyError('No such URI')
        except Exception, e:
            self.response = "Can't resolve the request!"
            print 'Error while doing dispatch!', e


class EchoHandler(asyncore.dispatcher_with_send):
    def handle_read(self):
        data = self.recv(8192)
        if data:
            data_instance = AnswerRequest(data)
            data = data_instance.response
            self.send(data)


class EchoServer(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print 'Incoming connection from %s' % repr(addr)
            handler = EchoHandler(sock)


def main():
    print 'Running on 127.0.0.1:8080 (Press CTRL+C to quit)'
    server = EchoServer('localhost', 8080)
    asyncore.loop()


def sample_foo(val):
    print 'hello,', val


if __name__ == '__main__':
    view_functions = {'hey': sample_foo}
    main()
