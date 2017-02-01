import json
from flask import Flask, redirect, url_for, session, Blueprint
from flask_oauth import OAuth
from urllib2 import Request, urlopen, URLError

import settings

auth_views = Blueprint('auth', __name__)
oauth = OAuth()

# You must configure these 3 values from Google APIs console
# https://code.google.com/apis/console
google = oauth.remote_app(
    'google',
    base_url='https://www.google.com/accounts/',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    request_token_url=None,
    request_token_params={
        'scope': 'https://www.googleapis.com/auth/userinfo.email',
        'response_type': 'code'},
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_method='POST',
    access_token_params={'grant_type': 'authorization_code'},
    consumer_key=settings.GOOGLE_CLIENT_ID,
    consumer_secret=settings.GOOGLE_CLIENT_SECRET)

class Unauthorized(Exception):
    pass


def get_google_userinfo():
    access_token = session.get('access_token')
    if access_token is None:
        raise Unauthorized()

    headers = {'Authorization': 'OAuth '+access_token[0]}
    req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
                  None, headers)
    try:
        res = urlopen(req)
    except URLError, e:
        # Unauthorized - bad token
        if e.code == 401:
            session.pop('access_token', None)
            raise Unauthorized()
    except Exception as e:
        print e
        print res.content

    user_info = json.loads(res.read())
    return user_info


@auth_views.route('/login')
def login():
    callback=url_for('auth.authorized', _external=True)
    return google.authorize(callback=callback)



@auth_views.route(settings.REDIRECT_URI)
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    return redirect(url_for('auth.login'))


@google.tokengetter
def get_access_token():
    return session.get('access_token')


def auth_required(view):

    def wrapper():
        try:
            get_google_userinfo()
        except Unauthorized:
            return redirect(url_for('auth.login'))
        return view()

    return wrapper
