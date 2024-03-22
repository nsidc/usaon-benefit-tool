from typing import Literal

import sqlalchemy
from flask import Blueprint, Response, abort, render_template, request, url_for
from flask_login import login_required
from flask_pydantic import validate
from pydantic import BaseModel

from usaon_benefit_tool import db
from usaon_benefit_tool._types import RoleName
from usaon_benefit_tool.forms import FORMS_BY_MODEL
from usaon_benefit_tool.models.tables import AssessmentNode, Link, Node
from usaon_benefit_tool.util.rbac import forbid_except_for_roles
from usaon_benefit_tool.util.sankey import (
    permitted_source_link_types,
    permitted_target_link_types,
)

assessment_node_bp = Blueprint(
    'node',
    __name__,
    url_prefix='/node/<int:node_id>',
)


@assessment_node_bp.route('/form', methods=['GET'])
@login_required
def form(assessment_id: int, node_id: int):
    """View assessment node object form."""
    assessment_node = _query_for_assessment_node(assessment_id, node_id)

    form = FORMS_BY_MODEL[type(assessment_node)](obj=assessment_node)
    del form.node

    return render_template(
        'assessment/_edit_node.html',
        form=form,
        assessment_id=assessment_id,
        node=assessment_node.node,
    )


class _QueryModel(BaseModel):
    direction: Literal["left", "right"]


@assessment_node_bp.route('/form_new_link', methods=['GET'])
@login_required
@validate()
def form_new_link(assessment_id: int, node_id: int, query: _QueryModel):
    """Display a form to add a new link (to the left or right) of the node."""
    assessment_node = _query_for_assessment_node(assessment_id, node_id)

    LinkForm = FORMS_BY_MODEL[Link]

    # FIXME: I think this conditional is horrible!!!
    permitted_types: set
    if query.direction == "left":
        permitted_types = permitted_source_link_types(assessment_node.node.type)
        form = LinkForm(target_assessment_node=assessment_node)
        not_already_linked_query_expr = ~AssessmentNode.output_links.any(
            Link.target_assessment_node_id == assessment_node.id,
        )
        form.target_assessment_node.render_kw = {'hidden': 'true'}
        remaining_field = form.source_assessment_node
    else:
        permitted_types = permitted_target_link_types(assessment_node.node.type)
        form = LinkForm(source_assessment_node=assessment_node)
        not_already_linked_query_expr = ~AssessmentNode.input_links.any(
            Link.source_assessment_node_id == assessment_node.id,
        )
        form.source_assessment_node.render_kw = {'hidden': 'true'}
        remaining_field = form.target_assessment_node

    # TODO: Should this be a QueryFactory at the Form level (in FORMS_BY_MODEL)?
    # Filter:
    remaining_field.query = AssessmentNode.query.filter_by(
        assessment_id=assessment_id,
    ).filter(
        # Not this node
        AssessmentNode.id != assessment_node.id,
        # Of an allowable type
        AssessmentNode.node.has(Node.type.in_(permitted_types)),
        # Not already linked to this node
        not_already_linked_query_expr,
    )

    # TODO: If no nodes match the query, display a message indicating what type of nodes
    #       must be created to be able to create a link to this node.

    return render_template(
        'assessment/_new_node_link.html',
        form=form,
        assessment_node=assessment_node,
    )


@assessment_node_bp.route('', methods=['PUT'])
@login_required
def put(assessment_id: int, node_id: int):
    """Update an AssessmentNode."""
    forbid_except_for_roles([RoleName.ADMIN, RoleName.RESPONDENT])

    assessment_node = _query_for_assessment_node(assessment_id, node_id)
    form = FORMS_BY_MODEL[type(assessment_node)](request.form, obj=assessment_node)

    if not form.validate():
        # TODO: Better messaging, HTMX communication
        return Response(status=400)

    form.populate_obj(assessment_node)
    db.session.add(assessment_node)
    db.session.commit()

    return Response(
        status=200,
        headers={
            'HX-Redirect': url_for(
                'assessment.get',
                assessment_id=assessment_id,
            ),
        },
    )


@assessment_node_bp.route('', methods=['DELETE'])
@login_required
def delete(assessment_id: int, node_id: int):
    """Delete node object from assessment."""
    forbid_except_for_roles([RoleName.ADMIN, RoleName.RESPONDENT])

    assessment_node = _query_for_assessment_node(assessment_id, node_id)

    db.session.delete(assessment_node)
    db.session.commit()

    return Response(
        status=200,
        headers={
            'HX-Redirect': url_for(
                'assessment.get',
                assessment_id=assessment_id,
            ),
        },
    )


def _query_for_assessment_node(assessment_id, node_id):
    try:
        return AssessmentNode.query.filter_by(
            assessment_id=assessment_id,
            node_id=node_id,
        ).one()
    except sqlalchemy.orm.exc.NoResultFound:
        abort(404)
