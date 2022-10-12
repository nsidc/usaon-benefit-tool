from flask import redirect, render_template, request, url_for
from flask_wtf import FlaskForm
from wtforms import TextAreaField, validators

from usaon_vta_survey import app, db
from usaon_vta_survey.models.tables import Survey


class NewSurveyForm(FlaskForm):
    notes = TextAreaField(
        'Notes',
        validators=[
            # Match length of relevant DB field:
            validators.Length(max=Survey.notes.property.columns[0].type.length),
            validators.DataRequired(),
        ],
    )


@app.route('/survey/new', methods=['GET', 'POST'])
def new_survey():
    form = NewSurveyForm()

    if form.validate_on_submit():
        # Insert to DB
        survey = Survey(notes=form.notes.data)
        db.session.add(survey)
        db.session.commit()

        return redirect(url_for('view_survey', survey_id=survey.id))

    return render_template('new_survey.html', form=form)


@app.route('/survey/<string:survey_id>')
def view_survey(survey_id):
    # Fetch survey by id
    survey = db.get_or_404(Survey, survey_id)

    return render_template('survey.html', survey=survey)
