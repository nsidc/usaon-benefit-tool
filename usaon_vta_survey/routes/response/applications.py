from flask import redirect, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, validators

from usaon_vta_survey import app, db
from usaon_vta_survey.models.tables import ResponseApplication, Survey


class NewApplicationForm(FlaskForm):
    name = StringField(
        'Application name',
        validators=[
            validators.DataRequired(),
            validators.Length(max=ResponseApplication.name.property.columns[0].type.length),
        ],
    )


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
