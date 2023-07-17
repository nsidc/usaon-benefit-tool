import os
import time

from flask import redirect, session, url_for
from flask_dance.contrib.google import google, make_google_blueprint

from usaon_vta_survey import app
from usaon_vta_survey.util.db.user import ensure_user_exists

blueprint = make_google_blueprint(
    client_id=os.getenv('USAON_VTA_GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('USAON_VTA_GOOGLE_CLIENT_SECRET'),
    scope=["profile", "email"],
)
app.register_blueprint(
    blueprint, url_prefix="/login"
)  


@app.route("/log-in")  # to change this to /login
def login():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    ensure_user_exists(resp.json())
    return "You are {email} on Google".format(email=resp.json()['email'])  # redirect()


@app.before_request
def before_request():
    """Handle expired google tokens as a pre-request hook."""
    if token := (s := session).get('google_oauth_token'):
        print("Token expiring in", token['expires_at'] - time.time())
        if time.time() >= token['expires_at']:
            del s['google_oauth_token']
