import os
import sys
import time
import signal
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
        self.worker_pids = []
        self.running = True
        self.worker_running = True

    def serve_forever(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(128)

        print_banner(self.host, self.port, self.workers)

        signal.signal(signal.SIGTERM, self._graceful_shutdown)
        signal.signal(signal.SIGINT, self._graceful_shutdown)

        for _ in range(self.workers):
            pid = os.fork()
            if pid == 0:
                self._run_worker()
                return
            else:
                self.worker_pids.append(pid)

        while self.running:
            try:
                pid, _ = os.waitpid(-1, os.WNOHANG)
                if pid > 0 and pid in self.worker_pids:
                    self.worker_pids.remove(pid)
            except ChildProcessError:
                break

        log("Master shutting down...")

        for pid in self.worker_pids:
            try:
                os.kill(pid, signal.SIGTERM)
            except ProcessLookupError:
                pass

        for pid in self.worker_pids:
            try:
                os.waitpid(pid, 0)
            except ChildProcessError:
                pass

        self.server_socket.close()

        log("All workers stopped.")
        sys.exit(0)

    def _run_worker(self):
        log("Worker started")

        signal.signal(signal.SIGTERM, self._worker_shutdown)

        wsgi_handler = WSGIHandler(self.app, self.host, self.port)

        self.server_socket.settimeout(1.0)

        while self.worker_running:
            try:
                client_socket, _ = self.server_socket.accept()
                self._handle_client(client_socket, wsgi_handler)
            except socket.timeout:
                continue
            except OSError:
                break

        log("Worker exiting")
        sys.exit(0)

    def _handle_client(self, client_socket, wsgi_handler):
        start_time = time.time()
        try:
            raw_data = client_socket.recv(4096)
            if not raw_data:
                return

            request = HTTPRequest(raw_data)
            response_obj = wsgi_handler.handle(request)
            response_bytes = response_obj.build()

            client_socket.sendall(response_bytes)

            duration = (time.time() - start_time) * 1000
            client_addr = client_socket.getpeername()

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

    def _graceful_shutdown(self, signum, frame):
        self.running = False

    def _worker_shutdown(self, signum, frame):
        self.worker_running = False
