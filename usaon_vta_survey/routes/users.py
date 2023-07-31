from flask import render_template

from usaon_vta_survey import app
from usaon_vta_survey.forms import RoleEdit
from usaon_vta_survey.models.tables import User


@app.route('/users')
def view_users():
    users = User.query.order_by(User.name).all()
    form = RoleEdit()
    return render_template(
        'users.html',
        users=users,
        form=form,
    )
