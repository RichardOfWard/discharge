import os
import time
from urllib2 import urlopen, HTTPError
from threading import Thread
from werkzeug.wrappers import Request
from werkzeug.exceptions import NotFound
from werkzeug.serving import run_simple, WSGIRequestHandler
from werkzeug.wsgi import get_path_info, wrap_file
import mimetypes


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


class StaticFilesMiddleWare():
    def __init__(self, application, site):
        self.application = application
        self.site = site
        self.context = None
        self.extra_files = []

    def __call__(self, environ, start_response):
        if self.context is None:
            self.context = self.site.build()

            for input_file in self.context.input_files:
                self.extra_files.append(
                    os.path.join(self.site.source_path, input_file))

        cleaned_path = get_path_info(environ)
        cleaned_path = cleaned_path.lstrip('/')
        cleaned_path = '/' + cleaned_path
        static_file_path = None
        if cleaned_path.lstrip('/') in self.context.output_files:
            static_file_path = cleaned_path
        elif cleaned_path.endswith('/'):
            try_cleaned_path = cleaned_path + 'index.html'
            if try_cleaned_path.lstrip('/') in self.context.output_files:
                static_file_path = try_cleaned_path

        if static_file_path is None:
            return self.application(environ, start_response)

        real_path = os.path.join(self.context.site.build_path,
                                 static_file_path.lstrip('/'))

        guessed_type = mimetypes.guess_type(real_path)
        mime_type = guessed_type[0] or 'text/plain'
        file_size = int(os.path.getsize(real_path))

        headers = [
            ('Content-Type', mime_type),
            ('Content-Length', str(file_size)),
        ]
        start_response('200 OK', headers)
        return wrap_file(environ, open(real_path, 'rb'))


class Server(Thread):

    def __init__(self, site, host='localhost', port=8000, use_reloader=False):
        super(Server, self).__init__()
        self.site = site
        self.host = host
        self.port = port
        self.use_reloader = use_reloader

    @Request.application
    def application(self, request):
        if request.path == '/!SHUTDOWN!':
            request.environ['werkzeug.server.shutdown']()
        return NotFound()

    def run(self):
        application = StaticFilesMiddleWare(self.application, self.site)
        extra_files = application.extra_files

        run_simple(
            self.host, self.port, application,
            request_handler=CustomRequestHandler,
            threaded=True,
            use_reloader=self.use_reloader,
            extra_files=extra_files,
            use_debugger=True,
        )

    def start(self, *args, **kwargs):
        ret = super(Server, self).start()
        wait = kwargs.pop('wait', False)
        if wait:
            self.wait_for_start()
        return ret

    def shutdown(self, wait=False):
        if self.is_alive():
            try:
                urlopen('http://%s:%s/!SHUTDOWN!' % (self.host, self.port))
            except HTTPError:
                pass
        if wait:
            self.wait_for_shutdown()
        self.join()

    def wait_for_start(self):
        tries = 500
        print "waiting..."
        while tries:
            try:
                urlopen('http://%s:%s/!PING!' % (self.host, self.port))
            except HTTPError:
                break
            except:
                pass
            tries -= 1
            time.sleep(0.01)

        if  not tries:
            raise Exception("Could not start server")

    def wait_for_shutdown(self):
        print "waiting..."
        tries = 500
        while tries:
            try:
                urlopen('http://%s:%s/!PING!' % (self.host, self.port))
            except HTTPError:
                pass
            except:
                break
            tries -= 1
            time.sleep(0.01)

        if not tries:
            raise Exception("Could not stop server")
