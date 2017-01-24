#!/usr/bin/env python
from flask import Flask, render_template, request, abort
import json
import os

app = Flask(__name__, static_url_path='/static')


@app.route('/')
@app.route('/dashboard')
def home():
    return render_template("dashboard.html")


def _dashboards_path(username="user"):
    path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "user_data/dashboards/{username}".format(username=username)
    )
    if not os.path.exists(path):
        os.makedirs(path)
    return path


@app.route('/ajax/dashboards', methods=['GET'])
def dashboards():
    dashboards = os.listdir(_dashboards_path())
    return json.dumps([os.path.splitext(dashboard)[0] for dashboard in dashboards])


@app.route('/ajax/dashboard/<slug>', methods=['POST'])
def save_dashboard(slug):
    filepath = os.path.join(_dashboards_path(), "{}.json".format(slug))
    if request.method == "POST":
        data = json.dumps(request.json, sort_keys=True, indent=4, separators=(',', ': '))
        with open(filepath, "w") as f:
            f.write(data)
        return ""
    abort(412)


@app.route('/ajax/dashboard/<slug>', methods=['GET'])
def load_dashboard(slug):
    filepath = os.path.join(_dashboards_path(), "{}.json".format(slug))
    if request.method == "GET":
        with open(filepath, "r") as f:
            return f.read()
    abort(412)


app.run(debug=True)
