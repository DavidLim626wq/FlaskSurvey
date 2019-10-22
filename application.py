import cs50
import csv
import time

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    name = request.form.get("name")
    sid = request.form.get("ID number")
    rank = ["Freshman","Sophomore","Junior","Senior","Grad Student","Other"][int(request.form.get("rank"))-1]
    service = request.form.get("service")
    timestmp = hex(int(time.strftime("%y%m%d%H%M%S")))[2:]

    if (not name or not rank or not service):
        return render_template("error.html", message="You didn't fill out the form")

    # if no ID is provided, then generate one automatically using a timestamp
    if not sid:
        sid = timestmp

    file = open("survey.csv", "a")
    writer = csv.writer(file)
    writer.writerow((name, sid, rank, service, timestmp))
    file.close()
    return redirect("/sheet")

@app.route("/sheet", methods=["GET"])
def get_sheet():
    file = open("survey.csv","r")
    reader = csv.reader(file)
    entry_line = list(reader)
    file.close()
    return render_template("sheet.html", entry_line=entry_line)

