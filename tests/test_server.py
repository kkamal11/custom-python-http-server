import time
import signal
import requests
import subprocess


SERVER_COMMAND = [
    "python3",
    "main.py",
    "examples.flask_app:app",
    "--workers",
    "1",
]


def start_server():
    process = subprocess.Popen(
        SERVER_COMMAND,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    time.sleep(1)
    return process


def stop_server(process):
    process.send_signal(signal.SIGINT)
    process.wait(timeout=5)


def test_basic_response():
    process = start_server()

    try:
        response = requests.get("http://127.0.0.1:8000/")
        assert response.status_code == 200
    finally:
        stop_server(process)


def test_stats_endpoint():
    process = start_server()

    try:
        response = requests.get("http://127.0.0.1:8000/test/2")
        assert response.status_code == 200
        assert response.text == f"Showing this after {2} seconds"
    finally:
        stop_server(process)


def test_multiple_requests():
    process = start_server()

    try:
        for _ in range(5):
            r = requests.get("http://127.0.0.1:8000/")
            assert r.status_code == 200
    finally:
        stop_server(process)
