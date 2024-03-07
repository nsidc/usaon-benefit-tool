from flask import Blueprint, Response, render_template, request, url_for
from flask_login import login_required

from usaon_benefit_tool import db
from usaon_benefit_tool.forms import FORMS_BY_MODEL
from usaon_benefit_tool.models.tables import Survey, SurveyDataProduct
from usaon_benefit_tool.util.authorization import limit_response_editors
from usaon_benefit_tool.util.sankey import sankey_subset

project_data_products_bp = Blueprint(
    'data_products',
    __name__,
    url_prefix='/data_products',
)
Form = FORMS_BY_MODEL[SurveyDataProduct]


@project_data_products_bp.route('', methods=['GET'])
@login_required
def get(project_id: str):
    """Return a page for managing data products associated with a project."""
    project = db.get_or_404(Survey, project_id)
    project_data_product = SurveyDataProduct(survey_id=project.id)

    form = Form(obj=project_data_product)
    return render_template(
        'project/data_products.html',
        form=form,
        project=project,
        data_products=project.data_products,
        sankey_series=sankey_subset(project, SurveyDataProduct),
    )


@project_data_products_bp.route('', methods=['POST'])
@login_required
def post(project_id: str):
    """Add a new data product to the project's collection."""
    limit_response_editors()
    project_data_product = SurveyDataProduct(survey_id=project_id)
    form = Form(request.form, obj=project_data_product)

    if form.validate():
        form.populate_obj(project_data_product)
        db.session.add(project_data_product)
        db.session.commit()

    return Response(
        status=201,
        headers={
            'HX-Redirect': url_for(
                'project.view_project_overview',
                project_id=project_id,
            ),
        },
    )


@project_data_products_bp.route('/form', methods=['GET'])
@login_required
def form(project_id: str):
    """Return a form to input a data product to add to the project's collection."""
    project_data_product = SurveyDataProduct(survey_id=project_id)
    form = Form(obj=project_data_product)

    return render_template(
        'project/_data_product.html',
        form=form,
        project_id=project_id,
    )
