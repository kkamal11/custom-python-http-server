import os
import datetime

VERSION = "0.1.0"


class Colors:
    GREEN = "\033[92m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


def print_banner(host, port, workers):
    print()
    print(f"{Colors.GREEN}{Colors.BOLD}🚀 Custom Server v{VERSION}{Colors.RESET}")
    print("─" * 48)
    print(f"{Colors.CYAN}Bind:{Colors.RESET}        http://{host}:{port}")
    print(f"{Colors.CYAN}Workers:{Colors.RESET}     {workers}")
    print(f"{Colors.CYAN}Master PID:{Colors.RESET}  {os.getpid()}")
    print(f"{Colors.CYAN}Mode:{Colors.RESET}        Prefork (sync)")
    print("─" * 48)
    print()


def log(message, level="INFO"):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    pid = os.getpid()

    if level == "ERROR":
        color = Colors.RED
    elif level == "WARN":
        color = Colors.YELLOW
    else:
        color = Colors.GREEN

    print(f"{color}[{now}] [PID {pid}] [{level}] {message}{Colors.RESET}")


import time


def print_request_log(client_addr, request, status_code, response_size, duration):
    now = time.strftime("%H:%M:%S")

    ip = client_addr[0]
    method = request.method
    path = request.path
    version = request.http_version

    print(
        f"[{now}] {ip} "
        f'"{method} {path} {version}" '
        f"{status_code} {response_size} "
        f"{duration:.2f}ms"
    )
