from flask import redirect, render_template, request, url_for

from usaon_vta_survey import app, db
from usaon_vta_survey._types import ObservingSystemType
from usaon_vta_survey.forms import FORMS_BY_MODEL
from usaon_vta_survey.models.tables import ResponseObservingSystem, Survey


@app.route('/response/<string:survey_id>/observing_systems', methods=['GET', 'POST'])
def view_response_observing_systems(survey_id: str):
    Form = FORMS_BY_MODEL[ResponseObservingSystem]
    survey = db.get_or_404(Survey, survey_id)
    response_observing_system = ResponseObservingSystem(
        response_id=survey.response_id,
        type=ObservingSystemType.other,
    )

    if request.method == 'POST':
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
        'response_observing_systems.html',
        form=form,
        survey=survey,
        response=survey.response,
        observing_systems=survey.response.observing_systems,
    )
