from flask import redirect, url_for

from usaon_vta_survey import app


@app.route('/')
def index():
    return redirect(url_for('view_surveys'))
