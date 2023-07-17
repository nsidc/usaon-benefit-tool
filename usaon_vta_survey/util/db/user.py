from usaon_vta_survey import db
from usaon_vta_survey.models.tables import User


def ensure_user_exists(google_json: dict) -> User:
    """Based on json response from google, ensure the db has the user.

    Note: Does this include user updates for something like a name change?
    """
    user = User(id=google_json['email'], name=google_json['name'])
    if user := db.session.get(User, user.id):
        return user
    else:
        db.session.add(user)
        db.session.commit()
        return user
