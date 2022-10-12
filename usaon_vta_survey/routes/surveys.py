from flask import render_template

from usaon_vta_survey import app


@app.route('/surveys')
def surveys():
    surveys = [1, 2]
    return render_template(
        'surveys.html',
        surveys=surveys,
    )
