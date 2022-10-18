from flask import redirect, render_template, request, url_for

from usaon_vta_survey import app, db
from usaon_vta_survey.forms import FORMS_BY_MODEL
from usaon_vta_survey.models.tables import Survey


@app.route('/survey/new', methods=['GET', 'POST'])
def new_survey():
    Form = FORMS_BY_MODEL[Survey]
    survey = Survey()

    if request.method == "POST":
        form = Form(request.form, obj=survey)

        if form.validate():
            # Insert to DB
            form.populate_obj(survey)
            db.session.add(survey)
            db.session.commit()

            return redirect(url_for('view_survey', survey_id=survey.id))

    else:
        form = Form(obj=survey)

    return render_template('new_survey.html', form=form)


@app.route('/survey/<string:survey_id>')
def view_survey(survey_id: str):
    # Fetch survey by id
    survey = db.get_or_404(Survey, survey_id)

    return render_template('survey.html', survey=survey)
