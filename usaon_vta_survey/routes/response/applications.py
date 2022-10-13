from flask import redirect, render_template, url_for

from usaon_vta_survey import app, db
from usaon_vta_survey.forms import NewApplicationForm
from usaon_vta_survey.models.tables import ResponseApplication, Survey


@app.route('/response/<string:survey_id>/applications', methods=['GET', 'POST'])
def view_response_applications(survey_id: str):
    form = NewApplicationForm()
    survey = db.get_or_404(Survey, survey_id)

    if form.validate_on_submit():
        response_application = ResponseApplication(
            name=form.name.data,
            response_id=survey.response.id,
        )
        db.session.add(response_application)
        db.session.commit()

        return redirect(url_for('view_response_applications', survey_id=survey.id))

    return render_template(
        'response_applications.html',
        form=form,
        survey=survey,
        response=survey.response,
        applications=survey.response.applications,
    )
