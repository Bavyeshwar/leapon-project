from flask import Flask, render_template, jsonify
from werkzeug.exceptions import HTTPException
import urllib.request, pgeocode, addfips
import json, csv

af = addfips.AddFIPS()
nomi = pgeocode.Nominatim("us")
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
@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")
@app.route("/about", methods=['GET'])
def about():
    return render_template("about.html")
@app.route("/events", methods=['GET'])
def events():
    return render_template("events.html")
@app.route("/awareness", methods=['GET'])
def awareness():
    return render_template("awareness.html")
@app.route("/data", methods=['GET'])
def radon_data():
    return render_template("radon_data.html")
@app.route("/data-api", methods=['GET'])
def radon_api():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTQ8bNIWD28VlL1RrDLiXcjPUT0GJwcnWg8A7HU0vff9r7QXU_VqJvNy1ucKxgvLQQnbajovpDc4xOH/pub?output=csv"
    response = urllib.request.urlopen(url)
    lines = [line.decode('utf-8') for line in response.readlines()]

    reader = csv.DictReader(lines)
    mapped_data = []
    for row in enumerate(reader):
        zip_code = str(row[1]["Postal Code"]).strip()
        location = nomi.query_postal_code(zip_code)
        current = row[1]
        current["County"] = location.county_name
        current["FIPS"] = af.get_county_fips(current["County"], state=current["State"])
        current.pop("Country")
        current.pop("Timestamp")
        current.pop("Data Collected")
        current.pop("Postal Code")
        if current["PM2.5 Level"] == "": current.pop("PM2.5 Level")
        if current["Notes"] == "": current.pop("Notes")
        if current["Radon Short-Term Average (pCi/L)"] == "": current.pop("Radon Short-Term Average (pCi/L)")
        if current["Radon Long-Term Average (pCi/L)"] == "": current.pop("Radon Long-Term Average (pCi/L)")
        mapped_data.append(current)

    df = None
    try:
        with open("static/data/radon_zones-spreadsheet.json", "r") as file:
            df = json.load(file)
    except Exception as e:
        print("Failed to send radon data: ", e)
    return jsonify({ "Leapon-Data": mapped_data, "EPA-Data": df["filtered-raw-data"] }), 201

if __name__ == '__main__':
    app.run(debug=True)