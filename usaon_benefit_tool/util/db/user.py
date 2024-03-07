from usaon_benefit_tool import db
from usaon_benefit_tool.models.tables import User


def ensure_user_exists(google_json: dict) -> User:
    """Based on json response from google, ensure the db has the user.

    Note: Does this include user updates for something like a name change?
    """
    user = User(email=google_json['email'], name=google_json['name'])

    # NOTE: Alternative form is pseudocode:
    #    try: query.filter_by(email == ...).one()
    #    except NoResultFound: insert
    user_db = db.session.query(User).filter(User.email == user.email).one_or_none()
    if user_db:
        return user_db
    else:
        db.session.add(user)
        db.session.commit()
        return user
