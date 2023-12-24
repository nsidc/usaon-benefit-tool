from flask import Blueprint, flash, render_template, request
from flask_login import current_user, login_required

from usaon_benefit_tool import db
from usaon_benefit_tool.constants import repo
from usaon_benefit_tool.forms import FORMS_BY_MODEL
from usaon_benefit_tool.models.tables import User


def _validate_role_change(user: User, form) -> None:
    if form.data['role'] != user.role and current_user.role_id != 'admin':
        raise RuntimeError("Only admins can edit users roles.")


user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('/<user_id>', methods=['POST', 'GET'])
@login_required
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
    return render_template('profile.html', form=form, user=user, url=repo.REPO_URL)
