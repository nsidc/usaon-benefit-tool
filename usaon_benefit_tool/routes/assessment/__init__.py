from flask import Blueprint, Response, render_template, request, url_for, flash
from flask_login import login_required

from usaon_benefit_tool import db
from usaon_benefit_tool.forms import FORMS_BY_MODEL
from usaon_benefit_tool.models.tables import Assessment

# from usaon_benefit_tool.routes.assessment.link import assessment_link_bp
from usaon_benefit_tool.routes.assessment.links import assessment_links_bp

# from usaon_benefit_tool.routes.assessment.node import assessment_node_bp
from usaon_benefit_tool.routes.assessment.nodes import (
    assessment_nodes_bp,
)
from usaon_benefit_tool.util.sankey import sankey

assessment_bp = Blueprint(
    'assessment',
    __name__,
    url_prefix='/assessment/<string:assessment_id>',
)
assessment_bp.register_blueprint(assessment_links_bp)
# assessment_bp.register_blueprint(assessment_link_bp)
assessment_bp.register_blueprint(assessment_nodes_bp)
# assessment_bp.register_blueprint(assessment_node_bp)


@assessment_bp.route('')
@login_required
def get(assessment_id: str):
    """Display the assessment overview."""
    assessment = db.get_or_404(Assessment, assessment_id)
    return render_template(
        'assessment/overview.html',
        assessment=assessment,
        sankey_series=sankey(assessment),
    )

@assessment_bp.route('/edit', methods=['POST','GET'])
@login_required
def edit(assessment_id: str):
    """Display the assessment overview."""
    Form = FORMS_BY_MODEL[Assessment]
    assessment = db.get_or_404(Assessment, assessment_id)

    if request.method == 'POST':
        form = Form(request.form, obj=assessment)
        if form.validate():
            form.populate_obj(assessment)
            db.session.add(assessment)
            db.session.commit()
            form.populate_obj(assessment)

            flash(f"You have updated {assessment.title}.", 'success')

            return render_template(
                'assessment/edit.html', form=form, assessment=assessment)
    form = Form(obj=assessment)
    return render_template(
        'assessment/edit.html',
        form=form,
        assessment=assessment,
    )

@assessment_bp.route('/user_guide', methods=['GET'])
@login_required
def user_guide(assessment_id: str):
    """Display the assessment user guide."""
    assessment = db.get_or_404(Assessment, assessment_id)
    return render_template(
        'assessment/user_guide.html',
        assessment=assessment,
    )
