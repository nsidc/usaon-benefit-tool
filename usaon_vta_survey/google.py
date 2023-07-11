from flask import Flask, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google

app = Flask(__name__)
app.secret_key = "supersekrit"
blueprint = make_google_blueprint(
    client_id="647009865175-v434gk8eifs6ct8flrkqknm7dvl51oj8.apps.googleusercontent.com",
    client_secret="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",
    scope=["profile", "email"]
)
app.register_blueprint(blueprint, url_prefix="/login")

@app.route("/")
def index():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/plus/v1/people/me")
    assert resp.ok, resp.text
    return "You are {email} on Google".format(email=resp.json()["emails"][0]["value"])

if __name__ == "__main__":
    app.run()
