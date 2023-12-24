from flask import Blueprint, render_template
from flask_login import login_required

from usaon_benefit_tool.constants import repo
from usaon_benefit_tool.models.tables import Survey

surveys_bp = Blueprint('surveys', __name__, url_prefix='/surveys')


@surveys_bp.route('')
@login_required
def view_surveys():
    surveys = Survey.query.order_by(Survey.created_timestamp).all()
    return render_template('surveys.html', surveys=surveys, url=repo.REPO_URL)
