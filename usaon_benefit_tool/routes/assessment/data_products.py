from flask import Blueprint, Response, render_template, request, url_for
from flask_login import login_required

from usaon_benefit_tool import db
from usaon_benefit_tool.forms import FORMS_BY_MODEL
from usaon_benefit_tool.models.tables import Assessment, AssessmentDataProduct
from usaon_benefit_tool.util.authorization import limit_response_editors
from usaon_benefit_tool.util.sankey import sankey_subset

assessment_data_products_bp = Blueprint(
    'data_products',
    __name__,
    url_prefix='/data_products',
)
Form = FORMS_BY_MODEL[AssessmentDataProduct]


@assessment_data_products_bp.route('', methods=['GET'])
@login_required
def get(assessment_id: str):
    """Return a page for managing data products associated with a assessment."""
    assessment = db.get_or_404(Assessment, assessment_id)
    assessment_data_product = AssessmentDataProduct(assessment_id=assessment.id)

    form = Form(obj=assessment_data_product)
    return render_template(
        'assessment/data_products.html',
        form=form,
        assessment=assessment,
        data_products=assessment.data_products,
        sankey_series=sankey_subset(assessment, AssessmentDataProduct),
    )


@assessment_data_products_bp.route('', methods=['POST'])
@login_required
def post(assessment_id: str):
    """Add a new data product to the assessment's collection."""
    limit_response_editors()
    assessment_data_product = AssessmentDataProduct(assessment_id=assessment_id)
    form = Form(request.form, obj=assessment_data_product)

    if form.validate():
        form.populate_obj(assessment_data_product)
        db.session.add(assessment_data_product)
        db.session.commit()

    return Response(
        status=201,
        headers={
            'HX-Redirect': url_for(
                'assessment.view_assessment_overview',
                assessment_id=assessment_id,
            ),
        },
    )


@assessment_data_products_bp.route('/form', methods=['GET'])
@login_required
def form(assessment_id: str):
    """Return a form to input a data product to add to the assessment's collection."""
    assessment_data_product = AssessmentDataProduct(assessment_id=assessment_id)
    form = Form(obj=assessment_data_product)

    return render_template(
        'assessment/_data_product.html',
        form=form,
        assessment_id=assessment_id,
    )
