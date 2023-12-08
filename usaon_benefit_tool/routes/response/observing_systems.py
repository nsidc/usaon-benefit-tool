from flask import Blueprint, redirect, render_template, request, url_for

from usaon_benefit_tool import db
from usaon_benefit_tool._types import ObservingSystemType
from usaon_benefit_tool.forms import FORMS_BY_MODEL
from usaon_benefit_tool.models.tables import ResponseObservingSystem, Survey
from usaon_benefit_tool.util.authorization import limit_response_editors

observing_system_bp = Blueprint(
    'obs', __name__, url_prefix='/response/<string:survey_id>/observing_systems'
)


@observing_system_bp.route('', methods=['GET', 'POST'])
def view_response_observing_systems(survey_id: str):
    """View and add to observing systems associated with a response."""
    Form = FORMS_BY_MODEL[ResponseObservingSystem]
    survey = db.get_or_404(Survey, survey_id)
    response_observing_system = ResponseObservingSystem(
        response_id=survey.response_id,
        type=ObservingSystemType.other,
    )

    if request.method == 'POST':
        limit_response_editors()
        form = Form(request.form, obj=response_observing_system)

        if form.validate():
            form.populate_obj(response_observing_system)
            db.session.add(response_observing_system)
            db.session.commit()

            redirect_url = url_for(
                'obs.view_response_observing_systems',
                survey_id=survey.id,
            )
            return redirect(redirect_url)

    form = Form(obj=response_observing_system)
    return render_template(
        'response/observing_systems.html',
        form=form,
        survey=survey,
        response=survey.response,
        observing_systems=survey.response.observing_systems,
    )


@observing_system_bp.route('/<int:response_observing_system_id>', methods=['DELETE'])
def delete_response_observing_system(survey_id: int, response_observing_system_id: int):
    """Delete observing system response object from survey."""
    survey = db.get_or_404(Survey, survey_id)
    response_observing_system = db.get_or_404(
        ResponseObservingSystem, response_observing_system_id
    )
    db.session.delete(response_observing_system)
    db.session.commit()

    return redirect(
        url_for('obs.view_response_observing_systems', survey_id=survey.id),
        code=303,
    )
