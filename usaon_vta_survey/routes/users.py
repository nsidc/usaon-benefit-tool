from flask import render_template
from flask_login import login_required

from usaon_vta_survey import app
from usaon_vta_survey.models.tables import User


@app.route('/users')
@login_required
def view_users():
    users = User.query.order_by(User.name).all()
    return render_template(
        'users.html',
        users=users,
    )
