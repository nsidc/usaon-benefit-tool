from flask import redirect, render_template, request, url_for
from flask_login import login_required

from usaon_vta_survey import app, db
from usaon_vta_survey.forms import FORMS_BY_MODEL
from usaon_vta_survey.models.tables import (
    ResponseSocietalBenefitArea,
    SocietalBenefitArea,
    Survey,
)
from usaon_vta_survey.util.authorization import limit_response_editors


@app.route(
    '/response/<string:survey_id>/societal_benefit_areas', methods=['GET', 'POST']
)
@login_required
def view_response_sbas(survey_id: str):
    """View and add to observing systems associated with a response."""
    sbas = SocietalBenefitArea.query.all()
    Form = FORMS_BY_MODEL[ResponseSocietalBenefitArea]
    survey = db.get_or_404(Survey, survey_id)
    # show the list of available SBAs
    response_societal_benefit_area = ResponseSocietalBenefitArea(
        response_id=survey.response_id
    )

    if request.method == 'POST':
        limit_response_editors()
        form = Form(request.form, obj=response_societal_benefit_area)

        if form.validate():
            form.populate_obj(response_societal_benefit_area)
            db.session.add(response_societal_benefit_area)
            db.session.commit()

        return redirect(url_for('view_response_sbas', survey_id=survey.id))

    form = Form(obj=response_societal_benefit_area)
    return render_template(
        'response/sbas.html',
        form=form,
        survey=survey,
        sbas=sbas,
        response=survey.response,
        societal_benefit_areas=survey.response.societal_benefit_areas,
    )
