from flask import Blueprint, Response, render_template, request, url_for
from flask_login import login_required
from flask_pydantic import validate
from pydantic import BaseModel

from usaon_benefit_tool import db
from usaon_benefit_tool._types import NodeType, RoleName
from usaon_benefit_tool.forms import FORMS_BY_MODEL
from usaon_benefit_tool.models.tables import AssessmentNode, Node
from usaon_benefit_tool.util.rbac import forbid_except_for_roles

assessment_nodes_bp = Blueprint('nodes', __name__, url_prefix='/nodes')


@assessment_nodes_bp.route('', methods=['POST'])
@login_required
def post(assessment_id: str):
    """Add an entry to the assessment's node collection."""
    forbid_except_for_roles([RoleName.ADMIN, RoleName.RESPONDENT])

    cls = AssessmentNode 

    assessment_node = cls(assessment_id=assessment_id)
    form = FORMS_BY_MODEL[cls](request.form, obj=assessment_node)

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


# class _QueryModel(BaseModel):
#     node_type: NodeType


@assessment_nodes_bp.route('/form', methods=['GET'])
@login_required
@validate()
def form(assessment_id: str, query: _QueryModel):
    """Return a form to add an entry to the assessment's nodes collection."""
    cls = AssessmentNode
    assessment_node = cls(assessment_id=assessment_id)
    form = FORMS_BY_MODEL[cls](obj=assessment_node)

    form.node.query = Node.query.filter_by(
        # Select only nodes that are of the selected type
        type=query.node_type,
    ).filter(
        # Select only nodes that are not already in this assessement
        Node.id.not_in(
            AssessmentNode.query.with_entities(
                AssessmentNode.node_id,
            ).filter_by(assessment_id=assessment_id),
        ),
    )

    post_url = url_for(
        'assessment.nodes.post',
        assessment_id=assessment_id,
        node_type=query.node_type.value,
    )
    return render_template(
        'partials/modal_search_form.html',
        title=f"Add {query.node_type.replace('_', ' ')} node",
        form_attrs=f"hx-post={post_url}",
        form=form,
    )
