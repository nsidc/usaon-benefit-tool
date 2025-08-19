from flask import Blueprint, Response, render_template, request, url_for
from flask_login import login_required
from flask_pydantic import validate
from pydantic import BaseModel

from usaon_benefit_tool import db
from usaon_benefit_tool._types import NodeType, RoleName
from usaon_benefit_tool.forms import FORMS_BY_MODEL
from usaon_benefit_tool.models.tables import Node
from usaon_benefit_tool.util.node_type import get_node_class_by_type
from usaon_benefit_tool.util.rbac import forbid_except_for_roles

# NB: The user facing term for "nodes" is "objects"
nodes_bp = Blueprint('nodes', __name__, url_prefix='/objects')


@nodes_bp.route('', methods=["GET"])
@login_required
def get():
    nodes = Node.query.order_by(Node.created_timestamp).all()
    return render_template(
        'nodes.html',
        nodes=nodes,
    )


@nodes_bp.route('', methods=["POST"])
@login_required
def post():
    """Add a node to the collection."""
    forbid_except_for_roles([RoleName.ADMIN, RoleName.RESPONDENT])

    # TODO: How to avoid using request.args? Typing worked on the GET endpoint, but not
    #       this one.
    node_type = request.args.get("node_type")
    cls = get_node_class_by_type(NodeType(node_type))
    node = cls()
    form = FORMS_BY_MODEL[cls](request.form, obj=node)

    if not form.validate():
        # FIXME: Handle this case! Return an error code and let HTMX handle it?
        # breakpoint()
        raise RuntimeError("FIXME")

    # Insert to DB
    form.populate_obj(node)
    # HACK: This just feels hacky, can we do better?
    node.type = node_type

    db.session.add(node)
    db.session.commit()

    return Response(
        status=201,
        headers={'HX-Redirect': url_for('nodes.get')},
    )


class _QueryModel(BaseModel):
    node_type: NodeType


@nodes_bp.route('/form', methods=["GET"])
@login_required
@validate()
def form(query: _QueryModel):
    """Return a form for adding a node to the collection."""
    cls = get_node_class_by_type(query.node_type)
    form = FORMS_BY_MODEL[cls](obj=cls())

    post_url = url_for('nodes.post', node_type=query.node_type.value)
    return render_template(
        'partials/modal_form.html',
        title=f"New {query.node_type.value.replace('_', ' ')}",
        form_attrs=f"hx-post={post_url}",
        form=form,
        enable_search=False,
    )
