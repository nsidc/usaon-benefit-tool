from flask import render_template

from usaon_vta_survey import app
from usaon_vta_survey.models.tables import Survey


@app.route('/surveys')
def surveys():
    surveys = Survey.query.order_by(Survey.created_timestamp).all()
    return render_template(
        'surveys.html',
        surveys=surveys,
    )
