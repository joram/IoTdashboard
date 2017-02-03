#!/usr/bin/env python
import datetime
from flask import render_template, request, abort, Blueprint, redirect
import json
import os
from auth import get_google_userinfo, auth_required

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
    dashboard_titles = []
    dashboards = os.listdir(_dashboards_path())
    if len(dashboards) == 0:
        _save_dashboard(EXAMPLE_DASHBOARD)
    dashboards = os.listdir(_dashboards_path())

    for dashboard_filename in dashboards:
        filepath = os.path.join(_dashboards_path(), dashboard_filename)
        with open(filepath, "r") as f:
            data = json.loads(f.read())
            title = data['title']
            slug = data['slug']
            dashboard_titles.append({'title': title, 'slug': slug})
    return json.dumps(dashboard_titles)


@dashboard_views.route('/ajax/dashboard', methods=['POST'])
def create_dashboard():
    data = dict(EXAMPLE_DASHBOARD)
    data['slug'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _save_dashboard(data)
    return data['slug']


@dashboard_views.route('/ajax/dashboard/<slug>', methods=['POST'])
def save_dashboard(slug):
    if request.method == "POST":
        _save_dashboard(request.json)
        return request.json['slug']
    abort(412)


@dashboard_views.route('/ajax/dashboard/<slug>', methods=['GET'])
def load_dashboard(slug):
    filepath = os.path.join(_dashboards_path(), "{}.json".format(slug))
    if request.method == "GET":
        with open(filepath, "r") as f:
            return f.read()
    abort(412)

