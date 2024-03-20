from flask import abort
from flask_login import current_user

from usaon_benefit_tool._types import RoleName


def forbid_except_for_roles(
    allowed_roles: list[RoleName],
    *,
    message: str | None = None,
) -> None:
    """Abort with a 403 except for the roles passed in."""
    if not current_user.is_authenticated:
        abort(403, description="Must be logged in.")

    allowed_role_names = [rn.value for rn in allowed_roles]
    out_msg = f"You must be one of the following roles: {allowed_role_names}"
    if message:
        out_msg = f"{message}. {out_msg}"

    if current_user.role_id not in allowed_roles:
        abort(403, out_msg)
