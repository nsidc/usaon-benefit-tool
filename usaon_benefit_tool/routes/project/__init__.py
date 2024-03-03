from flask import Blueprint, render_template
from flask_login import login_required

from usaon_benefit_tool import db
from usaon_benefit_tool.models.tables import Survey
from usaon_benefit_tool.routes.project.data_product import project_data_product_bp
from usaon_benefit_tool.routes.project.data_products import project_data_products_bp
from usaon_benefit_tool.util.sankey import sankey

project_bp = Blueprint('project', __name__, url_prefix='/project/<string:project_id>')
project_bp.register_blueprint(project_data_product_bp)
project_bp.register_blueprint(project_data_products_bp)


@project_bp.route('', methods=['GET'])
@login_required
def view_project(project_id: str):
    """Display the project user guide."""
    project = db.get_or_404(Survey, project_id)

    return render_template(
        'project/user_guide.html',
        project=project,
        response=project.response,
        sankey_series=sankey(project.response),
    )


@project_bp.route('/overview')
@login_required
def view_project_overview(project_id: str):
    """Display the project overview."""
    project = db.get_or_404(Survey, project_id)
    sankey_series = sankey(project.response) if project.response else []

    return render_template(
        'project/overview.html',
        project=project,
        sankey_series=sankey_series,
    )


@project_bp.route('/edit')
@login_required
def edit_project(project_id: str):
    """Display an interface for editing a project.

    TODO: Only permit respondents
    """
    project = db.get_or_404(Survey, project_id)
    sankey_series = sankey(project.response) if project.response else []

    return render_template(
        'project/edit.html',
        project=project,
        sankey_series=sankey_series,
    )
