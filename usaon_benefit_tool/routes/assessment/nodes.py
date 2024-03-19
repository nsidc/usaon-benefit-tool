from flask import Blueprint, Response, render_template, request, url_for
from flask_login import login_required

from usaon_benefit_tool import db
from usaon_benefit_tool.forms import FORMS_BY_MODEL
from usaon_benefit_tool.models.tables import AssessmentNode, Node

assessment_nodes_bp = Blueprint('nodes', __name__, url_prefix='/nodes')
Form = FORMS_BY_MODEL[AssessmentNode]


# @assessment_nodes_bp.route('', methods=['GET'])
# @login_required
# def get(assessment_id: str):
#     """Return a page for managing data products associated with a assessment."""
#     assessment = db.get_or_404(Assessment, assessment_id)
#     assessment_data_product = AssessmentDataProduct(assessment_id=assessment.id)
#
#     form = Form(obj=assessment_data_product)
#     return render_template(
#         'assessment/nodes.html',
#         form=form,
#         assessment=assessment,
#         nodes=assessment.nodes,
#         sankey_series=sankey_subset(assessment, AssessmentDataProduct),
#     )


@assessment_nodes_bp.route('', methods=['POST'])
@login_required
def post(assessment_id: str):
    """Add an entry to the assessment's node collection."""
    assessment_node = AssessmentNode(assessment_id=assessment_id)
    form = Form(request.form, obj=assessment_node)

    if form.validate():
        form.populate_obj(assessment_node)
        db.session.add(assessment_node)
        db.session.commit()

    return Response(
        status=201,
        headers={
            'HX-Redirect': url_for(
                'assessment.get',
                assessment_id=assessment_id,
            ),
        },
    )


@assessment_nodes_bp.route('/form', methods=['GET'])
@login_required
def form(assessment_id: str):
    """Return a form to add an entry to the assessment's nodes collection."""
    assessment_node = AssessmentNode(assessment_id=assessment_id)
    form = Form(obj=assessment_node)

    # List only nodes that are not already in this assessement!
    form.node.query = Node.query.filter(
        Node.id.not_in(
            AssessmentNode.query.with_entities(
                AssessmentNode.node_id,
            ).filter_by(assessment_id=assessment_id),
        ),
    )

    post_url = url_for('assessment.nodes.post', assessment_id=assessment_id)

    return render_template(
        'partials/modal_form.html',
        title="Add a node",
        form_attrs=f"hx-post={post_url}",
        form=form,
    )
