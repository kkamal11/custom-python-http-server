import sys
import importlib
from src.server import HTTPServer


def load_app(app_path: str):
    """
    Load WSGI app from string like: module:app
    """
    if ":" not in app_path:
        raise ValueError("App must be in format module:callable")

    module_name, app_name = app_path.split(":", 1)

    module = importlib.import_module(module_name)
    app = getattr(module, app_name)

    return app, app_name


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 main.py module:app")
        sys.exit(1)

    app_path = sys.argv[1]
    app, app_name = load_app(app_path)
    print(f"Starting application {app_name} on custom server")

    server = HTTPServer(app=app)
    server.serve_forever()
