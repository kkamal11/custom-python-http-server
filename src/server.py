import os
import time
import socket
from src.request import HTTPRequest
from src.wsgi import WSGIHandler
from src.cli import print_banner, log, print_request_log


class HTTPServer:
    def __init__(self, host="127.0.0.1", port=8000, app=None, workers=1):
        self.host = host
        self.port = port
        self.app = app
        self.workers = workers

    def serve_forever(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(128)

        print_banner(self.host, self.port, self.workers)

        for _ in range(self.workers):
            pid = os.fork()

            if pid == 0:
                # Child process (worker)
                self._run_worker(server_socket)
                return

        # Master just waits
        while True:
            os.wait()

    def _run_worker(self, server_socket):
        log("Worker started")
        wsgi_handler = WSGIHandler(self.app, self.host, self.port)

        while True:
            client_socket, _ = server_socket.accept()
            self._handle_client(client_socket, wsgi_handler)

    def _handle_client(self, client_socket, wsgi_handler):
        try:
            start_time = time.time()

            client_addr = client_socket.getpeername()

            raw_data = client_socket.recv(4096)
            if not raw_data:
                return

            request = HTTPRequest(raw_data)

            response_obj = wsgi_handler.handle(request)
            response_bytes = response_obj.build()

            client_socket.sendall(response_bytes)

            duration = (time.time() - start_time) * 1000

            print_request_log(
                client_addr,
                request,
                response_obj.status_code,
                len(response_obj.body),
                duration,
            )

        except Exception as e:
            log(f"Worker error: {e}", level="ERROR")

        finally:
            client_socket.close()
