from flask import Blueprint, render_template

from usaon_vta_survey.models.tables import Survey

surveys_bp = Blueprint('surveys', __name__, url_prefix='/surveys')


@surveys_bp.route('')
def view_surveys():
    surveys = Survey.query.order_by(Survey.created_timestamp).all()
    return render_template(
        'surveys.html',
        surveys=surveys,
    )
