import os

from flask import redirect, url_for
from flask_dance.contrib.google import google, make_google_blueprint

from usaon_vta_survey import app

blueprint = make_google_blueprint(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
    scope=["profile", "email"],
)
app.register_blueprint(
    blueprint, url_prefix="/login"
)  # can we make this something other than login


@app.route("/")  # to change this to /login
def login():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    # "You are {email} on Google".format(email=resp.json()['emails'])
    return "You are {email} on Google".format(email=resp.json()['email'])  # redirect()


if __name__ == "__main__":
    app.run()
