from flask import render_template, request
from flask_login import LoginManager, current_user

from usaon_vta_survey import app, db
from usaon_vta_survey.forms import FORMS_BY_MODEL
from usaon_vta_survey.models.tables import User

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id: str) -> User:
    return User.query.get(user_id)


def _validate_role_change(user: User, form) -> None:
    if not form.data['role_id'] == user.role_id and not current_user.role_id == 'admin':
        raise RuntimeError("Only admins can edit users roles.")


@app.route('/user/<user_id>', methods=['POST', 'GET'])
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

            return render_template('profile.html', form=form, user=user)
    form = Form(obj=user)
    return render_template('profile.html', form=form, user=user)
