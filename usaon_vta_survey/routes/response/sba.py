from flask import render_template

from usaon_vta_survey import app, db
from usaon_vta_survey.models.tables import SocietalBenefitArea, Survey


@app.route(
    '/response/<string:survey_id>/societal_benefit_areas', methods=['GET', 'POST']
)
def view_response_sba(survey_id: str):
    """View and add to observing systems associated with a response."""
    survey = db.get_or_404(Survey, survey_id)
    sbas = SocietalBenefitArea.query.all()

    return render_template(
        'response/sba.html',
        survey=survey,
        sbas=sbas,
    )
