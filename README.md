# 🚀 MiniGunicorn – Custom WSGI HTTP Server

A minimal Gunicorn-like WSGI HTTP server built from scratch in Python.

This project demonstrates:

- ✅ Raw TCP HTTP server
- ✅ HTTP request parsing
- ✅ WSGI compatibility (Flask supported)
- ✅ Prefork worker model
- ✅ Graceful shutdown
- ✅ Access logging
- ✅ Keep-Alive support
- ✅ CLI interface
- ✅ Production-style architecture

---

## 📦 Project Structure

```bash
custom-server/
│
├── src/
│ ├── server.py         # Core prefork server
│ ├── request.py        # HTTP request parser
│ ├── response.py       # HTTP response builder
│ ├── wsgi.py           # WSGI bridge
│ ├── cli.py            # Logging & CLI utilities
│ └── config.py         # Central configuration
│
├── examples/
│ └── flask_app.py      # Example Flask app
│
├── main.py             # CLI entry point
├── requirements.txt
└── README.md
```

## 🛠 Installation

### 1️⃣ Clone Repository

```bash
git clone git@github.com:kkamal11/custom-python-http-server.git
cd root_directory
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate 
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

To run with Default Settings:

```bash
python main.py examples.flask_app:app
```

To run with custom host and port:

```bash
python main.py examples.flask_app:app --host 127.0.0.1 --port 8080
```

To run with multiple workers:

```bash
python main.py examples.flask_app:app --workers 4
```

To run with a custom WSGI app:

```bash
python main.py module:callable_app
```

## 🧪 Example Flask App

```python
# examples/flask_app.py
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from Custom MiniGunicorn!"
```

## 🧪 Example Django App

```python
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse
from django.urls import path
settings.configure(
    DEBUG=True,
    SECRET_KEY="super-secret-key-1234567890$@qwertyuiop",
    ROOT_URLCONF=__name__,
    ALLOWED_HOSTS=["*"],
    MIDDLEWARE=[],
)
def home(request):
    return HttpResponse("Hello from Django via MiniGunicorn!")
urlpatterns = [
    path("", home),
]
app = get_wsgi_application()
```

## 📊 Access Logs

Logs are printed to the console in Common Log Format:

```bash
[12:44:12] 127.0.0.1 "GET / HTTP/1.1" 200 42 0.75ms
```

## 🏗 Architecture

- **main.py**: CLI entry point, argument parsing, app loading
- **server.py**: Prefork server, worker management, request handling
- **request.py**: HTTP request parsing
- **response.py**: HTTP response building
- **wsgi.py**: WSGI bridge to call the app
- **cli.py**: Logging and CLI utilities
- **config.py**: Central configuration constants

It uses a prefork worker model:

```bash
Master Process
    ├── Worker 1
    ├── Worker 2
    ├── Worker 3
    └── Worker N
```
Master process listens for incoming connections and dispatches them to worker processes. Each worker handles requests independently, allowing for concurrent processing.

## 🛑 Graceful Shutdown

The server can be gracefully shut down using `Ctrl+C`. The master process will signal all worker processes to terminate, allowing them to finish processing any ongoing requests before exiting.

## ⚙ CLI Options

```bash
Usage:
  python main.py module:app [OPTIONS]

Options:
  --host       Bind host (default: 127.0.0.1)
  --port       Bind port (default: 8000)
  --workers    Number of worker processes (default: 1)
  --help       Show help message
```

## ⚠️ Limitations

This is a minimal implementation for educational purposes. It lacks many features of a production server like Gunicorn, such as:

- SSL/TLS support
- Advanced error handling
- Configuration files
- Signal handling for worker management
- Support for async workers
- Profound Middleware support
- Extensive logging options
- Performance optimizations
- Security hardening

**I made it it as a learning tool and a starting point for building a more robust server and get to know how does a production WSGI server work!**

## 🧑‍💻 Author

Kamal Kishor – [GitHub](https://github.com/kkamal11)
