class HTTPRequest:
    def __init__(self, raw_data: bytes):
        self.raw = raw_data
        self.method = None
        self.path = None
        self.http_version = None
        self.headers = {}
        self.body = b""
        self.query_string = ""

        self._parse()

    def _parse(self):
        request_text = self.raw.decode("utf-8", errors="ignore")
        lines = request_text.split("\r\n")

        # Request line
        request_line = lines[0]
        self.method, full_path, self.http_version = request_line.split()
        if "?" in full_path:
            self.path, self.query_string = full_path.split("?", 1)
        else:
            self.path = full_path
            self.query_string = ""

        # Headers
        index = 1
        while lines[index]:
            key, value = lines[index].split(":", 1)
            self.headers[key.strip()] = value.strip()
            index += 1

        # Body (if any)
        body_index = request_text.find("\r\n\r\n")
        if body_index != -1:
            self.body = self.raw[body_index + 4 :]
