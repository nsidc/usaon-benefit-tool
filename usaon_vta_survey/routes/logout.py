from flask import redirect
from flask_login import logout_user

from usaon_vta_survey.routes.root import root_blueprint


@root_blueprint.route("/logout")
def logout():
    logout_user()
    return redirect("/")
