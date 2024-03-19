from flask import Blueprint, Response, render_template, request, url_for
from flask_login import login_required

from usaon_benefit_tool import db
from usaon_benefit_tool.forms import FORMS_BY_MODEL
from usaon_benefit_tool.models.tables import Link

assessment_link_bp = Blueprint(
    'link',
    __name__,
    url_prefix='/link/<int:link_id>',
)
Form = FORMS_BY_MODEL[Link]


@assessment_link_bp.route('/form', methods=['GET'])
@login_required
def form(assessment_id: int, link_id: int):
    """View assessment node object."""
    link = db.get_or_404(Link, link_id)
    form = Form(obj=link)

    del form.source_assessment_node
    del form.target_assessment_node

    return render_template(
        'assessment/_edit_link.html',
        form=form,
        assessment_id=assessment_id,
        link=link,
    )


@assessment_link_bp.route('', methods=['PUT'])
@login_required
def put(assessment_id: int, link_id: int):
    link = db.get_or_404(Link, link_id)

    form = Form(request.form, obj=link)

    if not form.validate():
        # TODO: Better messaging, HTMX communication
        return Response(status=400)

    form.populate_obj(link)
    db.session.add(link)
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


@assessment_link_bp.route('', methods=['DELETE'])
@login_required
def delete(assessment_id: int, link_id: int):
    """Delete link between nodes."""
    link = db.get_or_404(Link, link_id)

    db.session.delete(link)
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
