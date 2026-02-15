import sys
import argparse
import importlib
from textwrap import dedent
from src.server import HTTPServer
from src.config import VERSION, DEFAULT_HOST, DEFAULT_PORT, DEFAULT_WORKERS

version = VERSION


def load_app(app_path: str):
    if ":" not in app_path:
        raise ValueError("App must be in format module:callable")

    module_name, app_name = app_path.split(":", 1)

    module = importlib.import_module(module_name)
    app = getattr(module, app_name)

    if not callable(app):
        raise TypeError(f"{app_name} is not callable")

    return app


def main():
    description = dedent(
        """
        Mini Gunicorn-like Custom WSGI Server

        The app should be provided as:
            module:callable

        Example:
            examples.flask_app:app
    """
    )

    epilog = dedent(
        """
        Examples:

          Run with default settings:
            python main.py examples.flask_app:app

          Run on all interfaces:
            python main.py examples.flask_app:app --host 0.0.0.0

          Run on custom port:
            python main.py examples.flask_app:app --port 9000

          Run with 4 workers:
            python main.py examples.flask_app:app --workers 4
    """
    )

    parser = argparse.ArgumentParser(
        prog="mini-gunicorn",
        description=description,
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("app", help="WSGI app in format module:callable")

    parser.add_argument(
        "--host", default=DEFAULT_HOST, help="Bind host (default: 127.0.0.1)"
    )

    parser.add_argument(
        "--port", type=int, default=DEFAULT_PORT, help="Bind port (default: 8000)"
    )

    parser.add_argument(
        "--workers",
        type=int,
        default=DEFAULT_WORKERS,
        help="Number of worker processes (default: 1)",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}",
    )

    args = parser.parse_args()

    try:
        app = load_app(args.app)
    except Exception as e:
        print(f"Error loading app: {e}")
        sys.exit(1)

    server = HTTPServer(
        host=args.host,
        port=args.port,
        app=app,
        workers=args.workers,
    )

    server.serve_forever()


if __name__ == "__main__":
    main()
