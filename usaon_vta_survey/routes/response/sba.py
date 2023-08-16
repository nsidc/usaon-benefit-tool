from flask import redirect, render_template, request, url_for

from usaon_vta_survey import app, db
from usaon_vta_survey.forms import FORMS_BY_MODEL
from usaon_vta_survey.models.tables import ResponseSocietalBenefitArea, Survey
from usaon_vta_survey.util.authorization import limit_response_editors


@app.route(
    '/response/<string:survey_id>/societal_benefit_areas', methods=['GET', 'POST']
)
def view_response_sba(survey_id: str):
    """View and add to observing systems associated with a response."""
    Form = FORMS_BY_MODEL[ResponseSocietalBenefitArea]
    survey = db.get_or_404(Survey, survey_id)
    response_sba = ResponseSocietalBenefitArea(response_id=survey.response_id)

    if request.method == 'POST':
        limit_response_editors()
        form = Form(request.form, obj=response_sba)

        if form.validate():
            form.populate_obj(response_sba)
            db.session.add(response_sba)
            db.session.commit()

            redirect_url = url_for(
                'view_response_sba',
                survey_id=survey.id,
            )
            return redirect(redirect_url)

    form = Form(obj=response_sba)
    return render_template(
        'response/sba.html',
        form=form,
        survey=survey,
        response=survey.response,
        sba=survey.response.sba,
    )
