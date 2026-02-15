import os

SERVER_NAME = "My Custom WSGI Server"
VERSION = "0.1.0"
DESCRIPTION = "Minimal Gunicorn-like custom WSGI Server"

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000
DEFAULT_WORKERS = 1
DEFAULT_BACKLOG = 128

MASTER_PID = os.getpid()
