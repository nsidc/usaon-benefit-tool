from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required

from usaon_benefit_tool import db
from usaon_benefit_tool.forms import FORMS_BY_MODEL
from usaon_benefit_tool.models.tables import Response, Survey
from usaon_benefit_tool.util.authorization import limit_response_editors
from usaon_benefit_tool.util.full_sankey import sankey

# TODO: we don't need both of these concepts.
response_bp = Blueprint('response', __name__, url_prefix='/response')
survey_bp = Blueprint('survey', __name__, url_prefix='/survey')


@response_bp.route('/<string:survey_id>', methods=['GET'])
@login_required
def view_response(survey_id: str):
    """View or create response to a survey."""
    # Anyone should be able to view a survey
    # Only admins or respondents should be able to create a response.
    survey = db.get_or_404(Survey, survey_id)
    limit_response_editors()

    return render_template(
        'survey/user_guide.html',
        survey=survey,
        response=survey.response,
        sankey_series=sankey(survey.response),
    )


@survey_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_survey():
    Form = FORMS_BY_MODEL[Survey]
    survey = Survey()

    if request.method == 'POST':
        form = Form(request.form, obj=survey)

        if form.validate():
            # Insert to DB
            # TODO: We don't need a response concept!
            form.populate_obj(survey)

            response = Response()
            survey.response = response

            db.session.add(survey)
            db.session.add(response)
            db.session.commit()

            return redirect(url_for('survey.view_survey', survey_id=survey.id))

    form = Form(obj=survey)
    return render_template('new_survey.html', form=form)


@survey_bp.route('/<string:survey_id>')
@login_required
def view_survey(survey_id: str):
    # Fetch survey by id
    survey = db.get_or_404(Survey, survey_id)

    return render_template(
        'survey/overview.html',
        survey=survey,
        sankey_series=sankey(survey.response) if survey.response else [],
    )
