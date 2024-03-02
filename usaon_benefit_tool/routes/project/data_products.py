from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required

from usaon_benefit_tool import db
from usaon_benefit_tool.forms import FORMS_BY_MODEL
from usaon_benefit_tool.models.tables import ResponseDataProduct, Survey
from usaon_benefit_tool.util.authorization import limit_response_editors
from usaon_benefit_tool.util.sankey import data_products_sankey

project_data_products_bp = Blueprint(
    'data_products',
    __name__,
    url_prefix='/data_products',
)


# TODO: Rename "response" things
@project_data_products_bp.route('', methods=['GET', 'POST'])
@login_required
def view_response_data_products(project_id: str):
    """View and add to data products associated with a response."""
    Form = FORMS_BY_MODEL[ResponseDataProduct]
    project = db.get_or_404(Survey, project_id)
    response_data_product = ResponseDataProduct(response_id=project.response_id)

    if request.method == 'POST':
        limit_response_editors()
        form = Form(request.form, obj=response_data_product)

        if form.validate():
            form.populate_obj(response_data_product)
            db.session.add(response_data_product)
            db.session.commit()

        return redirect(
            url_for('data_product.view_response_data_products', project_id=project.id),
        )

    form = Form(obj=response_data_product)
    return render_template(
        'project/data_products.html',
        form=form,
        project=survey,
        response=project.response,
        data_products=project.response.data_products,
        sankey_series=data_products_sankey(project.response),
    )
