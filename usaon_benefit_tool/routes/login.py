import os

from flask import Blueprint, redirect, url_for
from flask_dance.consumer import oauth_authorized
from flask_dance.contrib.google import google, make_google_blueprint
from flask_login import login_user

from usaon_benefit_tool.util.db.user import ensure_user_exists

login_bp = Blueprint('login', __name__, url_prefix='/login')
google_bp = make_google_blueprint(
    client_id=os.getenv('USAON_BENEFIT_TOOL_GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('USAON_BENEFIT_TOOL_GOOGLE_CLIENT_SECRET'),
    scope=["profile", "email"],
)


@login_bp.route("")
def login():
    if not google.authorized:
        return redirect(url_for("google.login"))

    return redirect(url_for('root.root'))


@oauth_authorized.connect_via(google_bp)
def google_logged_in(blueprint):
    # TODO: Flash a message?
    account_data = blueprint.session.get("/oauth2/v2/userinfo")

    user = ensure_user_exists(account_data.json())
    login_user(user)

    return redirect(url_for('root.root'))
