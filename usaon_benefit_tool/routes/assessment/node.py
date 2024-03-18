import sqlalchemy
from flask import Blueprint, Response, render_template, request, url_for
from flask_login import login_required

from usaon_benefit_tool import db
from usaon_benefit_tool.forms import FORMS_BY_MODEL
from usaon_benefit_tool.models.tables import AssessmentNode

assessment_node_bp = Blueprint(
    'node',
    __name__,
    url_prefix='/node',
)
Form = FORMS_BY_MODEL[AssessmentNode]


@assessment_node_bp.route(
    '/<int:node_id>/form',
    methods=['GET'],
)
@login_required
def form(assessment_id: int, node_id: int):
    """View assessment node object."""
    try:
        assessment_node = _query_for_assessment_node(assessment_id, node_id)
    except sqlalchemy.orm.exc.NoResultFound:
        return Response(status=404)

    form = Form(obj=assessment_node)

    return render_template(
        'assessment/_edit_node.html',
        form=form,
        assessment_id=assessment_id,
        node=assessment_node.node,
    )


@assessment_node_bp.route('/<int:node_id>', methods=['PUT'])
@login_required
def put(assessment_id: int, node_id: int):
    try:
        assessment_node = _query_for_assessment_node(assessment_id, node_id)
    except sqlalchemy.orm.exc.NoResultFound:
        return Response(status=404)

    form = Form(request.form, obj=assessment_node)

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
                'assessment.view_assessment_overview',
                assessment_id=assessment_id,
            ),
        },
    )


@assessment_node_bp.route(
    '/<int:node_id>',
    methods=['DELETE'],
)
@login_required
def delete(assessment_id: int, node_id: int):
    """Delete node object from assessment."""
    try:
        assessment_node = _query_for_assessment_node(assessment_id, node_id)
    except sqlalchemy.orm.exc.NoResultFound:
        return Response(status=404)

    db.session.delete(assessment_node)
    db.session.commit()

    return Response(
        status=200,
        headers={
            'HX-Redirect': url_for(
                'assessment.view_assessment_overview',
                assessment_id=assessment_id,
            ),
        },
    )


def _query_for_assessment_node(assessment_id, node_id):
    return AssessmentNode.query.filter_by(
        assessment_id=assessment_id,
        node_id=node_id,
    ).one()
