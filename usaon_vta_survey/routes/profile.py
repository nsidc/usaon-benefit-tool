from flask import redirect, session, url_for

from usaon_vta_survey import app, db

@app.route('/profile/<id>', methods=['POST','GET'])
def profile(id):
    id = db.session.get(User, user.id)
    

    return render_template('profile.html', user=user)
