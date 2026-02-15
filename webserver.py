import socket

HOST = ""  # Bind to all available network interfaces (same as "0.0.0.0")
PORT = 8888

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP Server
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print(f"Serving HTTP on port {PORT} ...")
while True:
    client_connection, client_address = listen_socket.accept()
    request_data = client_connection.recv(1024)
    decoded_request_data = request_data.decode("utf-8")
    print(decoded_request_data)

    body = "Hello, World!"
    http_response = f"""\
    HTTP/1.1 200 OK
    Content-Type: text/plain
    Content-Length: {len(body)}

    <h1>{body}</h1>
    """.encode(
        "utf-8"
    )

    client_connection.sendall(http_response)
    client_connection.close()
