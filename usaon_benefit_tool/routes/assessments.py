from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_required

from usaon_benefit_tool import db
from usaon_benefit_tool.forms import FORMS_BY_MODEL
from usaon_benefit_tool.models.tables import Assessment

assessments_bp = Blueprint('assesments', __name__, url_prefix='/asessments')


@assessments_bp.route('')
@login_required
def view_assessments():
    assessments = Assessment.query.order_by(Assessment.created_timestamp).all()
    form = FORMS_BY_MODEL[Assessment](obj=Assessment())
    return render_template('assessments.html', assessments=assessments, form=form)


@assessments_bp.route('', methods=["POST"])
@login_required
def add_assessment():
    assessment = Assessment()
    form = FORMS_BY_MODEL[Assessment](request.form, obj=assessment)

    if not form.validate():
        # FIXME: Handle this case! Return an error code and let HTMX handle it?
        # breakpoint()
        raise RuntimeError("FIXME")

    # Insert to DB
    form.populate_obj(assessment)

    db.session.add(assessment)
    db.session.commit()

    return redirect(url_for('assessment.view_assessment', assessment_id=assessment.id))
