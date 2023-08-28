from flask import render_template

from usaon_vta_survey import app


@app.route("/")
def root():
    return render_template(
        'home.html',
    )
