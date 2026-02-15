from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("home.html")


@app.route("/second-page")
def second_page():
    return render_template("second_page.html", page="Second Page")
