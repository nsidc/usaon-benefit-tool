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

projects_bp = Blueprint('projects', __name__, url_prefix='/projects')


@projects_bp.route('')
@login_required
def view_projects():
    projects = Assessment.query.order_by(Assessment.created_timestamp).all()
    form = FORMS_BY_MODEL[Assessment](obj=Assessment())
    return render_template('projects.html', projects=projects, form=form)


@projects_bp.route('', methods=["POST"])
@login_required
def add_project():
    survey = Assessment()
    form = FORMS_BY_MODEL[Assessment](request.form, obj=survey)

    if not form.validate():
        # FIXME: Handle this case! Return an error code and let HTMX handle it?
        # breakpoint()
        raise RuntimeError("FIXME")

    # Insert to DB
    survey = Assessment()
    form.populate_obj(survey)

    db.session.add(survey)
    db.session.commit()

    return redirect(url_for('project.view_project', project_id=survey.id))
