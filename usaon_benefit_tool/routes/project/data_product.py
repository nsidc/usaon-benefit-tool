from flask import Blueprint, Response, render_template, url_for
from flask_login import login_required

from usaon_benefit_tool import db
from usaon_benefit_tool.forms import FORMS_BY_MODEL
from usaon_benefit_tool.models.tables import ResponseDataProduct, Survey

project_data_product_bp = Blueprint(
    'data_product',
    __name__,
    url_prefix='/data_product',
)


@project_data_product_bp.route('/<int:project_data_product_id>', methods=['GET'])
@login_required
def get(project_id: int, project_data_product_id: int):
    """View project data product object."""
    Form = FORMS_BY_MODEL[ResponseDataProduct]
    project_data_product = db.get_or_404(ResponseDataProduct, project_data_product_id)
    form = Form(obj=project_data_product)

    return render_template(
        'project/_data_product.html',
        project_data_product=project_data_product,
        form=form,
    )


@project_data_product_bp.route('/<int:project_data_product_id>', methods=['DELETE'])
@login_required
def delete(project_id: int, project_data_product_id: int):
    """Delete data product project object from project."""
    project = db.get_or_404(Survey, project_id)
    project_data_product = db.get_or_404(ResponseDataProduct, project_data_product_id)
    db.session.delete(project_data_product)
    db.session.commit()

    return Response(
        status=202,
        headers={
            'HX-Redirect': url_for(
                'project.view_project_overview',
                project_id=project_id,
            ),
        },
    )
