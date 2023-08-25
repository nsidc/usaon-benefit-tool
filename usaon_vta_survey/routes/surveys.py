from flask import render_template
from flask_login import login_required

from usaon_vta_survey import app
from usaon_vta_survey.models.tables import Survey


@app.route('/')
@app.route('/surveys')
@login_required
def view_surveys():
    # NOTE: if we're logged out we don't want to talk to the DB at all.
    surveys = Survey.query.order_by(Survey.created_timestamp).all()
    return render_template(
        'surveys.html',
        surveys=surveys,
    )
