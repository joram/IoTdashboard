#!/usr/bin/env python
from flask import Flask, render_template, request, abort
import json
import os

from dashboard import dashboard_views
from auth import auth_views
import settings


app = Flask(__name__, static_url_path='/static')
app.debug = True
app.secret_key = settings.SECRET_KEY
app.register_blueprint(auth_views)
app.register_blueprint(dashboard_views)

if __name__ == "__main__":
    port = os.environ.get("PORT", 5000)
    app.run(host="0.0.0.0", port)
