import os

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    session,
    url_for,
)
from flask_dance.consumer import oauth_authorized
from flask_dance.contrib.google import make_google_blueprint
from flask_login import current_user, login_user

from usaon_benefit_tool.util.db.user import ensure_user_exists

login_bp = Blueprint('login', __name__, url_prefix='/login')
google_bp = make_google_blueprint(
    client_id=os.getenv('USAON_BENEFIT_TOOL_GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('USAON_BENEFIT_TOOL_GOOGLE_CLIENT_SECRET'),
    scope=["profile", "email"],
)


@login_bp.route("")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('root.root'))

    return render_template("login.html")


@oauth_authorized.connect_via(google_bp)
def google_logged_in(blueprint, token):  # noqa: ARG001
    account_data = blueprint.session.get("/oauth2/v2/userinfo")

    user = ensure_user_exists(account_data.json())
    login_user(user)
    flash("You are now logged in.")

    next_url = session.get("next")
    if next_url:
        return redirect(next_url)

    return redirect(url_for('root.root'),url=repo.REPO_URL)
