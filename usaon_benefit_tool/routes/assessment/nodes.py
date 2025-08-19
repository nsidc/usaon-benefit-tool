# Modified Flask routes for USAON searchable modal

from flask import Blueprint, Response, render_template, request, url_for, jsonify
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
    else:
        # Return form with validation errors
        post_url = url_for(
            'assessment.nodes.post',
            assessment_id=assessment_id,
            node_type=node_type,
        )
        return render_template(
            'partials/modal_form.html',
            title=f"Add {NodeType(node_type).replace('_', ' ')} node",
            form_attrs=f"hx-post={post_url}",
            form=form,
            assessment_id=assessment_id,
            node_type=node_type,
        )


class _QueryModel(BaseModel):
    node_type: NodeType


@assessment_nodes_bp.route('/form', methods=['GET'])
@login_required
@validate()
def form(assessment_id: str, query: _QueryModel):
    """Return a form to add an entry to the assessment's nodes collection."""
    cls = get_assessment_node_class_by_type(query.node_type)
    assessment_node = cls(assessment_id=assessment_id)
    form = FORMS_BY_MODEL[cls](obj=assessment_node)

    # Don't set form.node.query here anymore - we'll handle search via HTMX
    # Remove or comment out this section:
    # form.node.query = Node.query.filter_by(
    #     type=query.node_type,
    # ).filter(
    #     Node.id.not_in(
    #         AssessmentNode.query.with_entities(
    #             AssessmentNode.node_id,
    #         ).filter_by(assessment_id=assessment_id),
    #     ),
    # )

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
        assessment_id=assessment_id,
        node_type=query.node_type.value,
    )


# New route for HTMX search
@assessment_nodes_bp.route('/search', methods=['POST'])
@login_required
def search_nodes(assessment_id: str):
    """Search for nodes that can be added to the assessment."""
    forbid_except_for_roles([RoleName.ADMIN, RoleName.RESPONDENT])
    
    search_term = request.form.get('search', '').strip()
    node_type = request.form.get('node_type')
    
    if not search_term or len(search_term) < 2:
        return ''  # Return empty if search term is too short
    
    # Build the same query as before, but with search filtering
    base_query = Node.query.filter_by(
        type=NodeType(node_type),
    ).filter(
        # Exclude nodes already in this assessment
        Node.id.not_in(
            AssessmentNode.query.with_entities(
                AssessmentNode.node_id,
            ).filter_by(assessment_id=assessment_id),
        ),
    )
    
    # Add search filtering using the correct field names from your Node model
    search_query = base_query.filter(
        db.or_(
            Node.title.ilike(f'%{search_term}%'),
            Node.short_name.ilike(f'%{search_term}%'),
            # Add other searchable fields as needed
        )
    ).limit(10)  # Limit results for performance
    
    results = search_query.all()
    
    if not results:
        return '<div class="p-3 text-muted text-center" style="font-style: italic;">No results found</div>'
    
    # Generate HTML for results using Bootstrap classes
    html_results = []
    for node in results:
        # Display ID and title
        display_text = f"#{node.id} - {node.title}"
        
        html_results.append(f'''
        <div class="p-3 border-bottom cursor-pointer" 
             style="cursor: pointer;" 
             onmouseover="this.style.backgroundColor='#f8f9fa'" 
             onmouseout="this.style.backgroundColor='white'"
             onclick="selectNode({node.id}, '{display_text}')">
            <strong>#{node.id}</strong> - {node.title}
        </div>
        ''')
    
    return ''.join(html_results)


# Optional: Endpoint to get node details
@assessment_nodes_bp.route('/node/<int:node_id>', methods=['GET'])
@login_required
def get_node_details(assessment_id: str, node_id: int):
    """Get details for a specific node."""
    node = Node.query.get_or_404(node_id)
    return {
        'id': node.id,
        'name': node.name,
        'description': node.description,
        'type': node.type.value if hasattr(node.type, 'value') else str(node.type),
    }
