from flask import render_template

from usaon_vta_survey.models.tables import Survey
from usaon_vta_survey.routes import root_blueprint


@root_blueprint.route('/surveys')
def view_surveys():
    surveys = Survey.query.order_by(Survey.created_timestamp).all()
    return render_template(
        'surveys.html',
        surveys=surveys,
    )
