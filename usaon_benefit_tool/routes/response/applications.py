from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required

from usaon_benefit_tool import db
from usaon_benefit_tool.forms import FORMS_BY_MODEL
from usaon_benefit_tool.models.tables import ResponseApplication, Survey
from usaon_benefit_tool.util.authorization import limit_response_editors
from usaon_benefit_tool.util.sankey import applications_sankey

application_bp = Blueprint(
    'application',
    __name__,
    url_prefix='/response/<int:survey_id>/applications',
)


@application_bp.route('', methods=['GET', 'POST'])
@login_required
def view_response_applications(survey_id: int):
    """View and add to applications associated with a response."""
    Form = FORMS_BY_MODEL[ResponseApplication]
    survey = db.get_or_404(Survey, survey_id)
    response_application = ResponseApplication(response_id=survey.response_id)

    if request.method == 'POST':
        limit_response_editors()
        form = Form(request.form, obj=response_application)

        if form.validate():
            form.populate_obj(response_application)
            db.session.add(response_application)
            db.session.commit()

        return redirect(
            url_for('application.view_response_applications', survey_id=survey.id),
        )

    form = Form(obj=response_application)
    return render_template(
        'response/applications.html',
        form=form,
        survey=survey,
        response=survey.response,
        applications=survey.response.applications,
        sankey_series=applications_sankey(survey.response),
    )


@application_bp.route('/<int:response_application_id>', methods=['DELETE'])
@login_required
def delete_response_application(survey_id: int, response_application_id: int):
    """Delete application response object from survey."""
    survey = db.get_or_404(Survey, survey_id)
    response_application = db.get_or_404(ResponseApplication, response_application_id)
    db.session.delete(response_application)
    db.session.commit()

    return redirect(
        url_for('application.view_response_applications', survey_id=survey.id),
        code=303,
    )
