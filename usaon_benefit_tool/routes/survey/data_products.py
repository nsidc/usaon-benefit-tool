from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required

from usaon_benefit_tool import db
from usaon_benefit_tool.forms import FORMS_BY_MODEL
from usaon_benefit_tool.models.tables import ResponseDataProduct, Survey
from usaon_benefit_tool.util.authorization import limit_response_editors
from usaon_benefit_tool.util.sankey import data_products_sankey

data_product_bp = Blueprint(
    'data_product',
    __name__,
    url_prefix='/response/<string:survey_id>/data_products',
)


@data_product_bp.route('', methods=['GET', 'POST'])
@login_required
def view_response_data_products(survey_id: str):
    """View and add to data products associated with a response."""
    Form = FORMS_BY_MODEL[ResponseDataProduct]
    survey = db.get_or_404(Survey, survey_id)
    response_data_product = ResponseDataProduct(response_id=survey.response_id)

    if request.method == 'POST':
        limit_response_editors()
        form = Form(request.form, obj=response_data_product)

        if form.validate():
            form.populate_obj(response_data_product)
            db.session.add(response_data_product)
            db.session.commit()

        return redirect(
            url_for('data_product.view_response_data_products', survey_id=survey.id),
        )

    form = Form(obj=response_data_product)
    return render_template(
        'survey/data_products.html',
        form=form,
        survey=survey,
        response=survey.response,
        data_products=survey.response.data_products,
        sankey_series=data_products_sankey(survey.response),
    )


@data_product_bp.route('/<int:response_data_product_id>', methods=['DELETE'])
@login_required
def delete_response_data_product(survey_id: int, response_data_product_id: int):
    """Delete data product response object from survey."""
    survey = db.get_or_404(Survey, survey_id)
    response_data_product = db.get_or_404(ResponseDataProduct, response_data_product_id)
    db.session.delete(response_data_product)
    db.session.commit()

    return redirect(
        url_for('data_product.view_response_data_products', survey_id=survey.id),
        code=303,
    )
