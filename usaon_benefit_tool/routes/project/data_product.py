from flask import Blueprint, Response, render_template, request, url_for
from flask_login import login_required

from usaon_benefit_tool import db
from usaon_benefit_tool.forms import FORMS_BY_MODEL
from usaon_benefit_tool.models.tables import AssessmentDataProduct

project_data_product_bp = Blueprint(
    'data_product',
    __name__,
    url_prefix='/data_product',
)
Form = FORMS_BY_MODEL[AssessmentDataProduct]


@project_data_product_bp.route('/<int:project_data_product_id>/form', methods=['GET'])
@login_required
def form(project_id: int, project_data_product_id: int):
    """View project data product object."""
    project_data_product = db.get_or_404(AssessmentDataProduct, project_data_product_id)
    form = Form(obj=project_data_product)

    return render_template(
        'project/_data_product.html',
        form=form,
        project_id=project_id,
        project_data_product_id=project_data_product_id,
    )


@project_data_product_bp.route('/<int:project_data_product_id>', methods=['PUT'])
@login_required
def put(project_id: int, project_data_product_id: int):
    project_data_product = db.get_or_404(
        AssessmentDataProduct,
        project_data_product_id,
    )
    form = Form(request.form, obj=project_data_product)

    if not form.validate():
        # TODO: Better messaging, HTMX communication
        return Response(status=400)

    form.populate_obj(project_data_product)
    db.session.add(project_data_product)
    db.session.commit()

    return Response(
        status=200,
        headers={
            'HX-Redirect': url_for(
                'project.view_project_overview',
                project_id=project_id,
            ),
        },
    )


@project_data_product_bp.route('/<int:project_data_product_id>', methods=['DELETE'])
@login_required
def delete(project_id: int, project_data_product_id: int):
    """Delete data product project object from project."""
    project_data_product = db.get_or_404(AssessmentDataProduct, project_data_product_id)
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
