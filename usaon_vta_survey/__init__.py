import os
from typing import Final

from flask import Flask
from flask_bootstrap import Bootstrap5
from sqlalchemy import inspect as sqla_inspect
from werkzeug.middleware.proxy_fix import ProxyFix

from usaon_vta_survey.constants.version import VERSION
from usaon_vta_survey.routes import root_blueprint
from usaon_vta_survey.util.db.connect import db_connstr
from usaon_vta_survey.util.envvar import envvar_is_true

__version__: Final[str] = VERSION


def create_app():
    """Create and configure the app."""
    # TODO: enable override config to test_config
    # https://flask.palletsprojects.com/en/2.3.x/tutorial/factory/

    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'youcanneverguess')
    app.config['LOGIN_DISABLED'] = envvar_is_true("USAON_VTA_LOGIN_DISABLED")
    app.config['SQLALCHEMY_DATABASE_URI'] = db_connstr(app)
    if envvar_is_true("USAON_VTA_PROXY"):
        app.wsgi_app = ProxyFix(app.wsgi_app, x_prefix=1)  # type: ignore

    from usaon_vta_survey.model import db

    db.init_app(app)
    Bootstrap5(app)

    app.register_blueprint(root_blueprint)

    app.jinja_env.globals.update(sqla_inspect=sqla_inspect, __version__=__version__)

    return app
