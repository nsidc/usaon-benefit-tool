from flask import render_template

from usaon_vta_survey import app


@app.route('/')
def index():
    return render_template('base.html')
