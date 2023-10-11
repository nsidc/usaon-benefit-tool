from flask import Blueprint, redirect, url_for
from flask_dance.contrib.google import google
from flask_login import login_user

from usaon_vta_survey.util.db.user import ensure_user_exists

login_bp = Blueprint('login', __name__, url_prefix='/login')


@login_bp.route("")
def login():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text

    user = ensure_user_exists(resp.json())
    login_user(user)

    return redirect(url_for('root.root'))


# this may be the login issue
# @app.before_request
# def before_request():
#     """Handle expired google tokens as a pre-request hook."""
#     if token := (s := session).get('google_oauth_token'):
#         print("Token expiring in", token['expires_at'] - time.time())
#         if time.time() >= token['expires_at']:
#             del s['google_oauth_token']
