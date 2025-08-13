from flask import Blueprint, Response, render_template, request, url_for
from flask_login import login_required
from flask_pydantic import validate
from pydantic import BaseModel

from usaon_benefit_tool import db
from usaon_benefit_tool._types import NodeType, RoleName
from usaon_benefit_tool.forms import FORMS_BY_MODEL
from usaon_benefit_tool.models.tables import AssessmentNode, Node
from usaon_benefit_tool.util.node_type import get_assessment_node_class_by_type
from usaon_benefit_tool.util.rbac import forbid_except_for_roles

assessment_nodes_bp = Blueprint('nodes', __name__, url_prefix='/nodes')


@assessment_nodes_bp.route('', methods=['POST'])
@login_required
def post(assessment_id: str):
    """Add an entry to the assessment's node collection."""
    forbid_except_for_roles([RoleName.ADMIN, RoleName.RESPONDENT])

    # TODO: How to avoid using request.args? Typing worked on the GET endpoint, but not
    #       this one.
    node_type = request.args.get("node_type")
    cls = get_assessment_node_class_by_type(NodeType(node_type))

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


class _QueryModel(BaseModel):
    node_type: NodeType


@assessment_nodes_bp.route('/form', methods=['GET'])
@login_required
@validate()
def form(assessment_id: str, query: _QueryModel):
    """Return a form to add an entry to the assessment's nodes collection."""
    search_query = request.args.get('search', '').strip()

    cls = get_assessment_node_class_by_type(query.node_type)
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

	if search_query:
		search_term = f"%{search_query.lower()}%"
		form.node.query = form.node.query.filter(
			Node.title.ilike(search_term)
	)

    post_url = url_for(
        'assessment.nodes.post',
        assessment_id=assessment_id,
        node_type=query.node_type.value,
    )
    return render_template(
        'partials/modal_form.html',
        title=f"Add {query.node_type.replace('_', ' ')} node",
        form_attrs=f"hx-post={post_url}",
        form=form,
    )
