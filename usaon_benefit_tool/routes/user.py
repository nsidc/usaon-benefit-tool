from flask import Blueprint, Response, flash, render_template, request
from flask_login import current_user, login_required

from usaon_benefit_tool import db
from usaon_benefit_tool._types import RoleName
from usaon_benefit_tool.forms import FORMS_BY_MODEL
from usaon_benefit_tool.models.tables import User
from usaon_benefit_tool.util.rbac import forbid_except_for_roles


def _validate_role_change(user: User, form) -> None:
    role_changed = form.data['role'] != user.role
    if role_changed and current_user.role_id != RoleName.ADMIN:
        # FIXME: abort(403) instead?
        raise RuntimeError("Only admins can edit users roles.")


user_bp = Blueprint('user', __name__, url_prefix='/user')
Form = FORMS_BY_MODEL[User]


@user_bp.route('/<user_id>', methods=['GET'])
@login_required
def get(user_id: str):
    user = db.get_or_404(User, user_id)
    form = Form(obj=user)

    return render_template('profile.html', form=form, user=user)


@user_bp.route('/<user_id>', methods=['POST'])
@login_required
def post(user_id: str):
    forbid_except_for_roles([RoleName.ADMIN])

    user = db.get_or_404(User, user_id)
    form = Form(request.form, obj=user)

    if not form.validate():
        # FIXME: Error handling!!
        return Response(400)

    _validate_role_change(user, form)
    form.populate_obj(user)
    db.session.add(user)
    db.session.commit()

    flash(f"You have updated {user.email}'s profile", 'success')

    return render_template('profile.html', form=form, user=user)
