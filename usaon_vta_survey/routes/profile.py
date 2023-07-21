from flask import render_template, request

from usaon_vta_survey import app, db
from usaon_vta_survey.forms import FORMS_BY_MODEL
from usaon_vta_survey.models.tables import User


@app.route('/profile/<user_id>', methods=['POST', 'GET'])
# Is a profile every really new??
# There will always be ID and NAME from google
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
    # at this point should there be a redirect or after submit is clicked?
    return render_template('profile.html', form=form)
