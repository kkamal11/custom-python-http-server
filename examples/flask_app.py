from flask import Flask

flask_app = Flask(__name__)


@flask_app.route("/")
def hello():
    return "Hello from Flask running on custom server!"
