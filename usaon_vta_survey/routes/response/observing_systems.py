from flask import redirect, render_template, request, url_for

from usaon_vta_survey import db
from usaon_vta_survey._types import ObservingSystemType
from usaon_vta_survey.forms import FORMS_BY_MODEL
from usaon_vta_survey.models.tables import ResponseObservingSystem, Survey
from usaon_vta_survey.routes import root_blueprint
from usaon_vta_survey.util.authorization import limit_response_editors


@root_blueprint.route(
    '/response/<string:survey_id>/observing_systems', methods=['GET', 'POST']
)
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
                'view_response_observing_systems',
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
