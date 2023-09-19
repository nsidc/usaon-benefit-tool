from flask import Blueprint, render_template

root_blueprint = Blueprint('root', __name__, url_prefix='/')


@root_blueprint.route('')
def root():
    return render_template(
        'home.html',
    )
