from flask import Blueprint, Response, render_template, request, url_for
from flask_login import login_required

from usaon_benefit_tool import db
from usaon_benefit_tool.forms import FORMS_BY_MODEL
from usaon_benefit_tool.models.tables import Survey, SurveyDataProduct
from usaon_benefit_tool.util.authorization import limit_response_editors
from usaon_benefit_tool.util.sankey import sankey_subset

assesment_data_products_bp = Blueprint(
    'data_products',
    __name__,
    url_prefix='/data_products',
)
Form = FORMS_BY_MODEL[SurveyDataProduct]


@assesment_data_products_bp.route('', methods=['GET'])
@login_required
def get(assesment_id: str):
    """Return a page for managing data products associated with a assesment."""
    assesment = db.get_or_404(Survey, assesment_id)
    assesment_data_product = SurveyDataProduct(survey_id=assesment.id)

    form = Form(obj=assesment_data_product)
    return render_template(
        'assesment/data_products.html',
        form=form,
        assesment=assesment,
        data_products=assesment.data_products,
        sankey_series=sankey_subset(assesment, SurveyDataProduct),
    )


@assesment_data_products_bp.route('', methods=['POST'])
@login_required
def post(assesment_id: str):
    """Add a new data product to the assesment's collection."""
    limit_response_editors()
    assesment_data_product = SurveyDataProduct(survey_id=assesment_id)
    form = Form(request.form, obj=assesment_data_product)

    if form.validate():
        form.populate_obj(assesment_data_product)
        db.session.add(assesment_data_product)
        db.session.commit()

    return Response(
        status=201,
        headers={
            'HX-Redirect': url_for(
                'assesment.view_assesment_overview',
                assesment_id=assesment_id,
            ),
        },
    )


@assesment_data_products_bp.route('/form', methods=['GET'])
@login_required
def form(assesment_id: str):
    """Return a form to input a data product to add to the assesment's collection."""
    assesment_data_product = SurveyDataProduct(survey_id=assesment_id)
    form = Form(obj=assesment_data_product)

    return render_template(
        'assesment/_data_product.html',
        form=form,
        assesment_id=assesment_id,
    )
