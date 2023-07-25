from flask import render_template, request
from flask_login import LoginManager

from usaon_vta_survey import app, db
from usaon_vta_survey.forms import FORMS_BY_MODEL
from usaon_vta_survey.models.tables import User

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id: str) -> User:
    return User.query.get(user_id)


@app.route('/profile/<user_id>', methods=['POST', 'GET'])
def profile(user_id: str):
    Form = FORMS_BY_MODEL[User]
    user = db.get_or_404(User, user_id)

    if request.method == 'POST':
        form = Form(request.form, obj=user)
        if form.validate():
            form.populate_obj(user)
            db.session.add(user)
            db.session.commit()

            return render_template('profile.html', form=form)
    form = Form(obj=user)
    return render_template('profile.html', form=form)
