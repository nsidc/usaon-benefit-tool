from flask import Blueprint, Response, render_template, request, url_for
from flask_login import login_required

from usaon_benefit_tool import db
from usaon_benefit_tool.forms import FORMS_BY_MODEL
from usaon_benefit_tool.models.tables import SurveyDataProduct

assesment_data_product_bp = Blueprint(
    'data_product',
    __name__,
    url_prefix='/data_product',
)
Form = FORMS_BY_MODEL[SurveyDataProduct]


@assesment_data_product_bp.route('/<int:assesment_data_product_id>/form', methods=['GET'])
@login_required
def form(assesment_id: int, assesment_data_product_id: int):
    """View assesment data product object."""
    assesment_data_product = db.get_or_404(SurveyDataProduct, assesment_data_product_id)
    form = Form(obj=assesment_data_product)

    return render_template(
        'assesment/_data_product.html',
        form=form,
        assesment_id=assesment_id,
        assesment_data_product_id=assesment_data_product_id,
    )


@assesment_data_product_bp.route('/<int:assesment_data_product_id>', methods=['PUT'])
@login_required
def put(assesment_id: int, assesment_data_product_id: int):
    assesment_data_product = db.get_or_404(
        SurveyDataProduct,
        assesment_data_product_id,
    )
    form = Form(request.form, obj=assesment_data_product)

    if not form.validate():
        # TODO: Better messaging, HTMX communication
        return Response(status=400)

    form.populate_obj(assesment_data_product)
    db.session.add(assesment_data_product)
    db.session.commit()

    return Response(
        status=200,
        headers={
            'HX-Redirect': url_for(
                'assesment.view_assesment_overview',
                assesment_id=assesment_id,
            ),
        },
    )


@assesment_data_product_bp.route('/<int:assesment_data_product_id>', methods=['DELETE'])
@login_required
def delete(assesment_id: int, assesment_data_product_id: int):
    """Delete data product assesment object from assesment."""
    assesment_data_product = db.get_or_404(SurveyDataProduct, assesment_data_product_id)
    db.session.delete(assesment_data_product)
    db.session.commit()

    return Response(
        status=202,
        headers={
            'HX-Redirect': url_for(
                'assesment.view_assesment_overview',
                assesment_id=assesment_id,
            ),
        },
    )
