class HTTPResponse:
    def __init__(self, status="200 OK", headers=None, body=b""):
        self.status = status
        self.headers = headers or []
        self.body = body

    @property
    def status_code(self):
        return int(self.status.split()[0])

    def build(self) -> bytes:
        response_line = f"HTTP/1.1 {self.status}\r\n"

        if not any(h[0].lower() == "content-length" for h in self.headers):
            self.headers.append(("Content-Length", str(len(self.body))))

        header_lines = ""
        for key, value in self.headers:
            header_lines += f"{key}: {value}\r\n"

        return response_line.encode() + header_lines.encode() + b"\r\n" + self.body
