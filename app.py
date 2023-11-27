"""Simple web interface for Psyreport"""

from flask import Flask, render_template, request

from psyreport import create_report

app = Flask(__name__)


@app.route("/")
def index():
    """Show the index page"""
    return render_template("index.html")


@app.route(
    "/generate",
    methods=[
        "POST",
    ],
)
def generate():
    """Generate the report from file"""
    report_file = request.files["report_file"]
    report = create_report(report_file, "plain.txt")
    return report, {"Content-Type": "text/text; charset=utf-8"}
