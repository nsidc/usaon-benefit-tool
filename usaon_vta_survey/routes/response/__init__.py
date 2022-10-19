from flask import render_template

from usaon_vta_survey import app, db
from usaon_vta_survey.models.tables import Response, Survey


@app.route('/response/<string:survey_id>', methods=['GET'])
def view_response(survey_id: str):
    """View or create response to a survey."""
    survey = db.get_or_404(Survey, survey_id)
    if not survey.response:
        response = Response()
        survey.response = response

        db.session.add(response)
        db.session.add(survey)
        db.session.commit()

    return render_template('response/view.html', survey=survey, response=survey.response)
