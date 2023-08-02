from flask_login import current_user


def limit_response_editors() -> None:
    if not (current_user.role_id == 'admin' or current_user.role_id == 'respondent'):
        raise RuntimeError(
            "You must be a respondent or admin to respond to this survey."
        )
