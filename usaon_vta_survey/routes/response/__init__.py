from flask import render_template
from flask_login import current_user

from usaon_vta_survey import app, db
from usaon_vta_survey.models.tables import Response, Survey


def _limit_response_editors() -> None:
    if not (current_user.role_id == 'admin' or current_user.role_id == 'respondent'):
        raise RuntimeError(
            "You must be a respondent or admin to respond to this survey."
        )


@app.route('/response/<string:survey_id>', methods=['GET'])
def view_response(survey_id: str):
    """View or create response to a survey."""
    # Anyone should be able to view a survey
    # Only admins or respondents should be able to create a response.
    survey = db.get_or_404(Survey, survey_id)
    if not survey.response:
        _limit_response_editors()
        response = Response()
        survey.response = response

        db.session.add(response)
        db.session.add(survey)
        db.session.commit()

    return render_template(
        'response/view.html',
        survey=survey,
        response=survey.response,
    )
