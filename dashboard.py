#!/usr/bin/env python
from flask import Flask, render_template, request, abort, Blueprint, redirect, url_for
import json
import os
from auth import get_google_userinfo, Unauthorized, auth_required

dashboard_views = Blueprint('dashboard_views', __name__)

EXAMPLE_DASHBOARD = {
  "slug": "default",
  "title": "Example dashboard",
  "panels": [
    {
      "title": "First Panel",
      "x": 1,
      "y": 1,
      "width": 5,
      "height": 5,
    }
  ],
}


@dashboard_views.route('/')
def landing():
    try:
        get_google_userinfo()
        return redirect("/dashboard")
    except:
        return render_template("landing.html")


@dashboard_views.route('/dashboard')
@auth_required
def dashboard():
    context = {
        "user": get_google_userinfo()
    }
    return render_template("dashboard.html", **context)


def _dashboards_path():
    username = get_google_userinfo().get("email")
    path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "user_data/dashboards/{username}".format(username=username)
    )
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def _save_dashboard(data):
    data_str = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
    filepath = os.path.join(_dashboards_path(), "{}.json".format(data.get("slug")))
    with open(filepath, "w") as f:
        f.write(data_str)


@dashboard_views.route('/ajax/dashboards', methods=['GET'])
def dashboards():
    dashboards = os.listdir(_dashboards_path())
    if len(dashboards) == 0:
      _save_dashboard(EXAMPLE_DASHBOARD)
      dashboards = os.listdir(_dashboards_path())
    return json.dumps([os.path.splitext(dashboard)[0] for dashboard in dashboards])


@dashboard_views.route('/ajax/dashboard/<slug>', methods=['POST'])
def save_dashboard(slug):
    if request.method == "POST":
        _save_dashboard(request.json)
        return ""
    abort(412)


@dashboard_views.route('/ajax/dashboard/<slug>', methods=['GET'])
def load_dashboard(slug):
    filepath = os.path.join(_dashboards_path(), "{}.json".format(slug))
    if request.method == "GET":
        with open(filepath, "r") as f:
            return f.read()
    abort(412)

