from flask_login import current_user


def limit_response_editors() -> None:
    if not current_user.is_authenticated:
        raise RuntimeError("Please login")
    if current_user.role_id not in ['admin', 'respondent']:
        raise RuntimeError(
            "You must be a respondent or admin to respond to this survey."
        )
