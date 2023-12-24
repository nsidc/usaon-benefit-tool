from flask import Blueprint, render_template
from usaon_benefit_tool.constants import repo

root_bp = Blueprint('root', __name__, url_prefix='/')


@root_bp.route('')
def root():
    return render_template('home.html',url=repo.REPO_URL)
