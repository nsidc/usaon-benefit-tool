from flask import Blueprint, render_template
from flask_login import login_required

from usaon_benefit_tool import db
from usaon_benefit_tool.models.tables import Survey
from usaon_benefit_tool.routes.assessment.data_product import project_data_product_bp
from usaon_benefit_tool.routes.assessment.data_products import project_data_products_bp
from usaon_benefit_tool.util.sankey import sankey

assessment_bp = Blueprint('assessment', __name__, url_prefix='/assessment/<string:assessment_id>')
assessment_bp.register_blueprint(project_data_product_bp)
assessment_bp.register_blueprint(project_data_products_bp)


@assessment_bp.route('/user_guide', methods=['GET'])
@login_required
def view_assessment(assessment_id: str):
    """Display the assessment user guide.

    TODO: Rename to "user_guide".
    """
    assessment = db.get_or_404(Survey, assessment_id)
    return render_template(
        'assessment/user_guide.html',
        assessment=assessment,
    )


@assessment_bp.route('')
@login_required
def view_assessment_overview(assessment_id: str):
    """Display the assessment overview.

    TODO: Rename to "get".
    """
    assessment = db.get_or_404(Survey, assessment_id)
    return render_template(
        'assessment/overview.html',
        assessment=assessment,
        sankey_series=sankey(assessment),
    )


@assessment_bp.route('/edit')
@login_required
def edit_assessment(assessment_id: str):
    """Display an interface for editing a assessment.

    TODO: Only permit respondents
    """
    assessment = db.get_or_404(Survey, assessment_id)
    return render_template(
        'assessment/edit.html',
        assessment=assessment,
        sankey_series=sankey(assessment),
    )
