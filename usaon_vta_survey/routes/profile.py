from flask import render_template, request

from usaon_vta_survey import app, db
from usaon_vta_survey.models.tables import User


@app.route('/profile/<id>', methods=['POST', 'GET'])
def profile(id):
    user = db.session.get(User, id)
    # breakpoint()
    if request.method == 'POST':
        user.biography = request.form['biography']
        user.orcid = request.form['orcid']
        user.affiliation = request.form['affiliation']

        db.session.add(user)
        db.session.commit()
        # return redirect(url_for('h'))

    return render_template('profile.html', user=user)
