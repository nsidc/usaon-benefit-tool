from flask import (
    Blueprint,
    render_template,
)
from flask_login import login_required

from usaon_benefit_tool.models.tables import Node

# NB: The user facing term for "nodes" is "objects"
nodes_bp = Blueprint('nodes', __name__, url_prefix='/objects')


@nodes_bp.route('', methods=["GET"])
@login_required
def get():
    nodes = Node.query.order_by(Node.created_timestamp).all()
    # form = FORMS_BY_MODEL[Node](obj=Node())
    return render_template(
        'nodes.html',
        nodes=nodes,
        # form=form,
    )
