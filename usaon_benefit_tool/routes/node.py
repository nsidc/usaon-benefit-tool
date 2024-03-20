from flask import Blueprint, Response, render_template, request, url_for
from flask_login import login_required

from usaon_benefit_tool import db
from usaon_benefit_tool._types import RoleName
from usaon_benefit_tool.forms import FORMS_BY_MODEL
from usaon_benefit_tool.models.tables import Node
from usaon_benefit_tool.util.rbac import forbid_except_for_roles

node_bp = Blueprint(
    'node',
    __name__,
    url_prefix='/object/<string:node_id>',
)


@node_bp.route('', methods=['GET'])
def get(node_id: str):
    """Display info about the node."""
    node = db.get_or_404(Node, node_id)
    form = FORMS_BY_MODEL[type(node)](obj=node)
    return render_template(
        'node.html',
        node=node,
        form=form,
    )


@node_bp.route('', methods=['DELETE'])
@login_required
def delete(node_id: str):
    """Delete the node."""
    forbid_except_for_roles([RoleName.ADMIN])

    node = db.get_or_404(Node, node_id)
    db.session.delete(node)
    db.session.commit()

    return Response(
        status=200,
        headers={'HX-Redirect': url_for('nodes.get')},
    )


@node_bp.route('', methods=['PUT'])
@login_required
def put(node_id: str):
    """Update the node."""
    forbid_except_for_roles([RoleName.ADMIN, RoleName.RESPONDENT])

    node = db.get_or_404(Node, node_id)
    form = FORMS_BY_MODEL[type(node)](request.form, obj=node)

    if not form.validate():
        # TODO: Better messaging, HTMX communication
        return Response(status=400)

    form.populate_obj(node)
    db.session.add(node)
    db.session.commit()

    return Response(
        status=200,
        headers={
            'HX-Redirect': url_for(
                'nodes.get',
            ),
        },
    )
