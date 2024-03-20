from flask import Blueprint, render_template
from flask_login import login_required

from usaon_benefit_tool._types import RoleName
from usaon_benefit_tool.models.tables import User
from usaon_benefit_tool.util.rbac import forbid_except_for_roles

users_bp = Blueprint('users', __name__, url_prefix='/users')


@users_bp.route('', methods=['GET'])
@login_required
def get():
    forbid_except_for_roles([RoleName.ADMIN])

    users = User.query.order_by(User.name).all()
    return render_template(
        'users.html',
        users=users,
    )
