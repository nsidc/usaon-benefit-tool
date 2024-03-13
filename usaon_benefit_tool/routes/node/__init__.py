from flask import Blueprint, Response, render_template, request, url_for
from flask_login import login_required

from usaon_benefit_tool import db
from usaon_benefit_tool.forms import FORMS_BY_MODEL
from usaon_benefit_tool.models.tables import Node

# TODO: Separate endpoints for each type of node? /node/data_product/...
#       Or /node/<node_id>?type=data_product or /node/<node_id/...?type=data_product
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
                'node.get',
                node_id=node_id,
            ),
        },
    )


# @node_bp.route('/form', methods=['GET'])
# @login_required
# def form(assessment_id: str):
#     """Display an interface for editing a assessment.
#
#     TODO: Only permit respondents
#     """
#     assessment = db.get_or_404(Assessment, assessment_id)
#     return render_template(
#         'assessment/edit.html',
#         assessment=assessment,
#         sankey_series=sankey(assessment),
#     )
