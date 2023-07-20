from flask import render_template, request

from usaon_vta_survey import app, db
from usaon_vta_survey.forms import FORMS_BY_MODEL
from usaon_vta_survey.models.tables import User


@app.route('/profile/<user_id>', methods=['POST', 'GET'])
# Is a profile every really new??
# There will always be ID and NAME from google
def profile(user_id: str):
    Form = FORMS_BY_MODEL[User]
    user = User()
    # breakpoint()

    if request.method == 'POST':
        form = Form(request.form, obj=user)
        if form.validate():
            form.populate_obj(user)
            db.session.add(user)
            db.session.commit()

            return render_template('profile.html', user_id=user.id)
    #  user.biography = request.form['biography']
    #  user.orcid = request.form['orcid']
    #  user.affiliation = request.form['affiliation']

    #  db.session.add(user)
    #  db.session.commit()
    # return redirect(url_for('surveys'))
    form = Form(obj=user)
    return render_template('new_profile.html', form=form)


@app.route('/profile/<id>')
def view_profile(user_id: str):
    # Fetch user by ID
    user = db.get_or_404(User, user_id)

    return render_template('profile_old.html', user=user)
