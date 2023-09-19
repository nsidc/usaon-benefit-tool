from flask import Blueprint, flash, render_template, request
from flask_login import current_user

from usaon_vta_survey import db
from usaon_vta_survey.forms import FORMS_BY_MODEL
from usaon_vta_survey.models.tables import User


def load_user(user_id: str) -> User:
    return User.query.get(user_id)


# TODO: figure out how to handle this with app factory
# if app.config["LOGIN_DISABLED"]:
#     # HACK: Always logged in as dev user when login is disabled
#     import flask_login.utils as flask_login_utils
#
#     from usaon_vta_survey.util.dev import DEV_USER
#
#     flask_login_utils._get_user = lambda: DEV_USER


def _validate_role_change(user: User, form) -> None:
    if not form.data['role'] == user.role_id and not current_user.role_id == 'admin':
        raise RuntimeError("Only admins can edit users roles.")


user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('/user/<user_id>', methods=['POST', 'GET'])
def user(user_id: str):
    Form = FORMS_BY_MODEL[User]
    user = db.get_or_404(User, user_id)

    if request.method == 'POST':
        form = Form(request.form, obj=user)
        if form.validate():
            _validate_role_change(user, form)
            form.populate_obj(user)
            db.session.add(user)
            db.session.commit()

            flash(f"You have updated {user.email}'s profile", 'success')

            return render_template('profile.html', form=form, user=user)
    form = Form(obj=user)
    return render_template('profile.html', form=form, user=user)
