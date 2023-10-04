from flask import Blueprint, render_template

from usaon_vta_survey import db
from usaon_vta_survey.models.tables import Response, Survey
from usaon_vta_survey.util.authorization import limit_response_editors
from usaon_vta_survey.util.full_sankey import sankey

response_bp = Blueprint('response', __name__, url_prefix='/response')


@response_bp.route('/<string:survey_id>', methods=['GET'])
def view_response(survey_id: str):
    """View or create response to a survey."""
    # Anyone should be able to view a survey
    # Only admins or respondents should be able to create a response.
    survey = db.get_or_404(Survey, survey_id)
    if not survey.response:
        limit_response_editors()
        response = Response()
        survey.response = response

        db.session.add(response)
        db.session.add(survey)
        db.session.commit()

    return render_template(
        'response/view.html',
        survey=survey,
        response=survey.response,
        sankey=sankey(survey.response),
    )
