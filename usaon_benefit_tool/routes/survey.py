from flask import Blueprint, redirect, render_template, request, url_for

from usaon_benefit_tool import db
from usaon_benefit_tool.forms import FORMS_BY_MODEL
from usaon_benefit_tool.models.tables import Survey

survey_bp = Blueprint('survey', __name__, url_prefix='/survey')


@survey_bp.route('/new', methods=['GET', 'POST'])
def new_survey():
    Form = FORMS_BY_MODEL[Survey]
    survey = Survey()

    if request.method == 'POST':
        form = Form(request.form, obj=survey)

        if form.validate():
            # Insert to DB
            form.populate_obj(survey)
            db.session.add(survey)
            db.session.commit()

            return redirect(url_for('survey.view_survey', survey_id=survey.id))

    form = Form(obj=survey)
    return render_template('new_survey.html', form=form)


@survey_bp.route('/<string:survey_id>')
def view_survey(survey_id: str):
    # Fetch survey by id
    survey = db.get_or_404(Survey, survey_id)

    return render_template('survey.html', survey=survey)
