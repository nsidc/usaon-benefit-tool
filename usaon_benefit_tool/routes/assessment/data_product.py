from flask import Blueprint, Response, render_template, request, url_for
from flask_login import login_required

from usaon_benefit_tool import db
from usaon_benefit_tool.forms import FORMS_BY_MODEL
from usaon_benefit_tool.models.tables import AssessmentDataProduct

assessment_data_product_bp = Blueprint(
    'data_product',
    __name__,
    url_prefix='/data_product',
)
Form = FORMS_BY_MODEL[AssessmentDataProduct]


@assessment_data_product_bp.route(
    '/<int:assessment_data_product_id>/form',
    methods=['GET'],
)
@login_required
def form(assessment_id: int, assessment_data_product_id: int):
    """View assessment data product object."""
    assessment_data_product = db.get_or_404(
        AssessmentDataProduct,
        assessment_data_product_id,
    )
    form = Form(obj=assessment_data_product)

    return render_template(
        'assessment/_data_product.html',
        form=form,
        assessment_id=assessment_id,
        assessment_data_product_id=assessment_data_product_id,
    )


@assessment_data_product_bp.route('/<int:assessment_data_product_id>', methods=['PUT'])
@login_required
def put(assessment_id: int, assessment_data_product_id: int):
    assessment_data_product = db.get_or_404(
        AssessmentDataProduct,
        assessment_data_product_id,
    )
    form = Form(request.form, obj=assessment_data_product)

    if not form.validate():
        # TODO: Better messaging, HTMX communication
        return Response(status=400)

    form.populate_obj(assessment_data_product)
    db.session.add(assessment_data_product)
    db.session.commit()

    return Response(
        status=200,
        headers={
            'HX-Redirect': url_for(
                'assessment.view_assessment_overview',
                assessment_id=assessment_id,
            ),
        },
    )


@assessment_data_product_bp.route(
    '/<int:assessment_data_product_id>',
    methods=['DELETE'],
)
@login_required
def delete(assessment_id: int, assessment_data_product_id: int):
    """Delete data product assessment object from assessment."""
    assessment_data_product = db.get_or_404(
        AssessmentDataProduct,
        assessment_data_product_id,
    )
    db.session.delete(assessment_data_product)
    db.session.commit()

    return Response(
        status=202,
        headers={
            'HX-Redirect': url_for(
                'assessment.view_assessment_overview',
                assessment_id=assessment_id,
            ),
        },
    )
