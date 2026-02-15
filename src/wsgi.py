import io
import sys
from .response import HTTPResponse


class WSGIHandler:
    def __init__(self, app, server_host, server_port):
        self.app = app
        self.server_host = server_host
        self.server_port = server_port

    def handle(self, request):
        environ = self._build_environ(request)
        headers_set = []

        def start_response(status, response_headers, exc_info=None):
            headers_set[:] = [status, response_headers]

        result = self.app(environ, start_response)

        status, response_headers = headers_set
        body = b"".join(result)

        response = HTTPResponse(
            status=status,
            headers=response_headers,
            body=body,
        )

        return response

    def _build_environ(self, request):
        environ = {}

        # CGI variables
        environ["REQUEST_METHOD"] = request.method
        environ["SCRIPT_NAME"] = ""
        environ["PATH_INFO"] = request.path
        environ["QUERY_STRING"] = getattr(request, "query_string", "")
        environ["SERVER_NAME"] = self.server_host
        environ["SERVER_PORT"] = str(self.server_port)
        environ["SERVER_PROTOCOL"] = request.http_version

        # WSGI variables
        environ["wsgi.version"] = (1, 0)
        environ["wsgi.url_scheme"] = "http"
        environ["wsgi.input"] = io.BytesIO(request.body)
        environ["wsgi.errors"] = sys.stderr
        environ["wsgi.multithread"] = False
        environ["wsgi.multiprocess"] = False
        environ["wsgi.run_once"] = False

        # HTTP headers
        for header, value in request.headers.items():
            key = "HTTP_" + header.upper().replace("-", "_")
            environ[key] = value

        return environ
