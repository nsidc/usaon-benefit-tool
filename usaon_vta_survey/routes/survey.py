from flask import redirect, render_template, url_for

from usaon_vta_survey import app, db
from usaon_vta_survey.forms import NewSurveyForm
from usaon_vta_survey.models.tables import Survey


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
def view_survey(survey_id: str):
    # Fetch survey by id
    survey = db.get_or_404(Survey, survey_id)

    return render_template('survey.html', survey=survey)
