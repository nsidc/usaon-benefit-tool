from flask import render_template

from usaon_vta_survey.routes import root_blueprint


@root_blueprint.route("/")
def root():
    return render_template(
        'home.html',
    )
