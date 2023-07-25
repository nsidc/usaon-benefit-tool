from flask import redirect
from flask_login import logout_user

from usaon_vta_survey import app


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")
