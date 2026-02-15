import socket
from .request import HTTPRequest
from .wsgi import WSGIHandler


class HTTPServer:
    def __init__(self, host="127.0.0.1", port=8000, app=None):
        self.host = host
        self.port = port
        self.app = app
        self.wsgi_handler = WSGIHandler(app, host, port)

    def serve_forever(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)

            print(f"Serving on http://{self.host}:{self.port}")

            while True:
                client_socket, addr = server_socket.accept()
                self._handle_client(client_socket)

    def _handle_client(self, client_socket):
        try:
            raw_data = client_socket.recv(4096)
            if not raw_data:
                return

            request = HTTPRequest(raw_data)

            if self.wsgi_handler:
                response = self.wsgi_handler.handle(request)
            else:
                response = b"HTTP/1.1 200 OK\r\n\r\nHello"

            client_socket.sendall(response)

        except Exception as e:
            print("Error:", e)

        finally:
            client_socket.close()
