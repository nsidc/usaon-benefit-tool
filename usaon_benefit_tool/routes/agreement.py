from datetime import UTC, datetime

from flask import Blueprint, flash, redirect, request, url_for
from flask_login import current_user, login_required, logout_user

from usaon_benefit_tool import db
from usaon_benefit_tool.constants.agreement import CURRENT_AGREEMENT_VERSION

agreement_bp = Blueprint('agreement', __name__, url_prefix='/agreement')


def user_needs_agreement(user) -> bool:
    """Is true if the user has not accepted the current agreement version."""
    return (
        user.is_authenticated
        and user.agreed_agreement_version != CURRENT_AGREEMENT_VERSION
    )


@agreement_bp.route("/accept", methods=["POST"])
@login_required
def accept():
    # Server-side validation: don't trust the client-side disabled button.
    if not request.form.get("agree"):
        flash(
            "You must check the box to accept the Contributor User" " Agreement.",
            "danger",
        )
        return redirect(url_for("root.root"))

    current_user.agreed_agreement_version = CURRENT_AGREEMENT_VERSION
    current_user.agreed_agreement_at = datetime.now(UTC)
    db.session.add(current_user)
    db.session.commit()

    flash("Thank you. You have accepted the Contributor User Agreement.")
    return redirect(url_for("root.root"))


@agreement_bp.route("/decline", methods=["POST"])
@login_required
def decline():
    """User chose not to accept: log them out rather than trapping them."""
    logout_user()
    flash(
        "You have not accepted the Contributor User Agreement, so you have"
        " been logged out. You may log in again at any time to review and"
        " accept it.",
    )
    return redirect(url_for("login.login"))
