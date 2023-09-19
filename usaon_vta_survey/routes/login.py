import os
import time

from flask import Blueprint, redirect, session, url_for
from flask_dance.contrib.google import google, make_google_blueprint
from flask_login import login_user

from usaon_vta_survey.util.db.user import ensure_user_exists

blueprint = make_google_blueprint(
    client_id=os.getenv('USAON_VTA_GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('USAON_VTA_GOOGLE_CLIENT_SECRET'),
    scope=["profile", "email"],
)

login_bp = Blueprint('login', __name__, url_prefix='/login')


@login_bp.route("")
def login():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text

    user = ensure_user_exists(resp.json())
    login_user(user)

    return redirect('/')


@login_bp.before_request
def before_request():
    """Handle expired google tokens as a pre-request hook."""
    if token := (s := session).get('google_oauth_token'):
        print("Token expiring in", token['expires_at'] - time.time())
        if time.time() >= token['expires_at']:
            del s['google_oauth_token']
