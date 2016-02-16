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

view_functions = {}


class AnswerRequest:
    def __init__(self, request):
        """
        Recv from the client request by socket!
        and then return the response to them as soon as possible!
        param::data; a string split by '|' character!
        """
        try:
            dispatch_instance = Dispatch(request)
            uri = dispatch_instance.message_id
            if uri in view_functions:
                # call app view functions here!
                self.response = view_functions[uri](dispatch_instance.request_dict)
            else:
                print 'No such URI'
        except Exception, e:
            self.response = "Can't resolve the request!"
            print 'Error while doing dispatch!', e

    def checking_device(self):
        """Called by the __init__ method, if the device id is no register
            just return False, else return True!
        """
        pass

    def checking_command(self):
        """Called by the __init__ method, if the command is right, just do
        it! else return to the client 'No such command'
        """
        pass


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


if __name__ == '__main__':
    main()
