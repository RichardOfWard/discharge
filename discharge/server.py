import os
import time
from urllib2 import urlopen, HTTPError
from threading import Thread
from werkzeug.wrappers import Request
from werkzeug.exceptions import NotFound
from werkzeug.serving import run_simple, WSGIRequestHandler


class CustomRequestHandler(WSGIRequestHandler):
    """Fixes Werkzeug's WSGIRequestHandler, which doesn't shut down
    properly on python 2.6
    """

    def initiate_shutdown(self):
        if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
            super(CustomRequestHandler, self).initiate_shutdown()
        else:
            self.server.shutdown()
            self.server.socket.close()


class Server(Thread):
    shutdown_flag = False

    def __init__(self, site, host='localhost', port=8000):
        super(Server, self).__init__()
        self.site = site
        self.host = host
        self.port = port

    @Request.application
    def application(self, request):
        if self.shutdown_flag:
            request.environ['werkzeug.server.shutdown']()
        return NotFound()

    def run(self):
        print {'/': self.site.build_path},
        run_simple(
            self.host, self.port, self.application,
            request_handler=CustomRequestHandler,
            threaded=True,
            static_files={'/': self.site.build_path},
        )

    def start(self, *args, **kwargs):
        ret = super(Server, self).start()
        # TODO: this is NOT a clean solution!
        # would be better to get run_simple emit a signal
        # when the socket is bound, which we can wait for here
        time.sleep(0.01)
        return ret

    def shutdown(self):
        self.shutdown_flag = True
        if self.is_alive():
            try:
                urlopen('http://%s:%s/!SHUTDOWN!' % (self.host, self.port))
            except HTTPError:
                pass
        self.join()
