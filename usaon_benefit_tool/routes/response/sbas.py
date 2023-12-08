from flask import Blueprint, redirect, render_template, request, url_for

from usaon_benefit_tool import db
from usaon_benefit_tool.forms import FORMS_BY_MODEL
from usaon_benefit_tool.models.tables import (
    ResponseSocietalBenefitArea,
    SocietalBenefitArea,
    Survey,
)
from usaon_benefit_tool.util.authorization import limit_response_editors
from usaon_benefit_tool.util.sankey import societal_benefit_areas_sankey

societal_benefit_area_bp = Blueprint(
    'sba', __name__, url_prefix='/response/<string:survey_id>/societal_benefit_areas'
)


@societal_benefit_area_bp.route('', methods=['GET', 'POST'])
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

        return redirect(url_for('sba.view_response_sbas', survey_id=survey.id))

    form = Form(obj=response_societal_benefit_area)
    return render_template(
        'response/sbas.html',
        form=form,
        survey=survey,
        sbas=sbas,
        response=survey.response,
        societal_benefit_areas=survey.response.societal_benefit_areas,
        sankey_series=societal_benefit_areas_sankey(survey.response),
    )


@societal_benefit_area_bp.route(
    '/<int:response_societal_benefit_area_id>', methods=['DELETE']
)
def delete_response_sba(survey_id: int, response_societal_benefit_area_id: int):
    """Delete societal benefit area response object from survey."""
    survey = db.get_or_404(Survey, survey_id)
    response_sba = db.get_or_404(
        ResponseSocietalBenefitArea, response_societal_benefit_area_id
    )
    db.session.delete(response_sba)
    db.session.commit()

    return redirect(
        url_for('sba.view_response_sbas', survey_id=survey.id),
        code=303,
    )
