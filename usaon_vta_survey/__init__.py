import os
from typing import Final

from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy import inspect as sqla_inspect
from werkzeug.middleware.proxy_fix import ProxyFix

from usaon_vta_survey.constants.version import VERSION
from usaon_vta_survey.util.db.connect import db_connstr
from usaon_vta_survey.util.envvar import envvar_is_true

__version__: Final[str] = VERSION


# TODO: Figure out where to put this. model.py?
# https://flask.palletsprojects.com/en/2.3.x/patterns/appfactories/#factories-extensions
db = SQLAlchemy(
    metadata=MetaData(
        naming_convention={
            'ix': 'ix_%(column_0_label)s',
            'uq': 'uq_%(table_name)s_%(column_0_name)s',
            'ck': 'ck_%(table_name)s_%(constraint_name)s',
            'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
            'pk': 'pk_%(table_name)s',
        }
    )
)


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

    db.init_app(app)
    Bootstrap5(app)

    from usaon_vta_survey.routes.root import root_blueprint

    app.register_blueprint(root_blueprint)

    from usaon_vta_survey.routes import response

    app.register_blueprint(response.bp)

    app.jinja_env.globals.update(sqla_inspect=sqla_inspect, __version__=__version__)

    return app
