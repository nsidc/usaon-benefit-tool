from flask import Blueprint, redirect
from flask_login import logout_user

logout_bp = Blueprint('logout', __name__, url_prefix='/logout')


@logout_bp.route("")
def logout():
    logout_user()
    return redirect("/")
