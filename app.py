from flask import Flask, render_template
from werkzeug.exceptions import HTTPException
import requests, json

app = Flask(__name__)

# Make sure nothing is cached.
@app.after_request
def no_cache(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Not Found
@app.errorhandler(HTTPException)
def error(e):
    code = e.code
    return render_template("error.html", error={"code": code, "name": e.name}), code
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/about")
def about():
    return render_template("about.html")
@app.route("/events")
def events():
    return render_template("events.html")
@app.route("/awareness")
def awareness():
    return render_template("awareness.html")
@app.route("/radon-levels")
def radon_data():
    return render_template("radon_data.html")

if __name__ == '__main__':
    app.run(debug=True)