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
from usaon_benefit_tool.models.tables import Response, Survey

projects_bp = Blueprint('projects', __name__, url_prefix='/projects')


@projects_bp.route('')
@login_required
def view_projects():
    projects = Survey.query.order_by(Survey.created_timestamp).all()
    form = FORMS_BY_MODEL[Survey](obj=Survey())
    return render_template('projects.html', projects=projects, form=form)


@projects_bp.route('', methods=["POST"])
@login_required
def add_project():
    survey = Survey()
    form = FORMS_BY_MODEL[Survey](request.form, obj=survey)

    if not form.validate():
        # TODO: Return an error code and let HTMX handle it?
        breakpoint()
        ...

    # Insert to DB
    survey = Survey()
    form.populate_obj(survey)

    response = Response()
    survey.response = response

    db.session.add(survey)
    db.session.add(response)
    db.session.commit()

    return redirect(url_for('project.view_project', project_id=survey.id))
