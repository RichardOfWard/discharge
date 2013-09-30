from urllib2 import urlopen, HTTPError
from discharge.server import Server

from .base import Test


class TestServer(Test):

    source_dir = 'test_server'

    def test_server_launch(self):
        server = Server(self.site)
        server.start()
        server.shutdown()

    def test_server_socket_shutdown(self):
        server = Server(self.site)
        server.start()
        server.shutdown()
        server = Server(self.site)
        server.start()
        server.shutdown()

    def test_server(self):
        self.site.build()
        server = Server(self.site)
        server.start()
        try:
            request = urlopen('http://localhost:8000/testfile.html')
            request.read()
        finally:
            server.shutdown()

    def test_index(self):
        self.site.build()
        server = Server(self.site)
        server.start()
        try:
            request = urlopen('http://localhost:8000/testdir/')
            request.read()
        finally:
            server.shutdown()

    def test_non_index(self):
        self.site.build()
        server = Server(self.site)
        server.start()
        try:
            request = urlopen('http://localhost:8000/')
            request.read()
        except HTTPError:
            pass
        else:
            assert False, "This request should be 404"
        finally:
            server.shutdown()
