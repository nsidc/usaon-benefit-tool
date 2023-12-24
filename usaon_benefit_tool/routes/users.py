from flask import Blueprint, render_template
from flask_login import login_required
from usaon_benefit_tool.constants import repo


from usaon_benefit_tool.models.tables import User

users_bp = Blueprint('users', __name__, url_prefix='/users')


@users_bp.route('')
@login_required
def view_users():
    users = User.query.order_by(User.name).all()
    return render_template(
        'users.html',
        users=users,
        url=repo.REPO_URL
    )
