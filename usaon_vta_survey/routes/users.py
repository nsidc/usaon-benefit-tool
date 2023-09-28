from flask import Blueprint, render_template

from usaon_vta_survey.models.tables import User

users_bp = Blueprint('users', __name__, url_prefix='/users')


@users_bp.route('')
def view_users():
    users = User.query.order_by(User.name).all()
    return render_template(
        'users.html',
        users=users,
    )
