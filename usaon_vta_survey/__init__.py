import os
import time
from typing import Final

from flask import Flask, session
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
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
    login_manager = LoginManager()
    login_manager.init_app(app)

    from usaon_vta_survey.models.tables import User

    @login_manager.user_loader
    def load_user(user_id: str) -> User:
        return User.query.get(user_id)

    @app.before_request
    def before_request():
        """Handle expired google tokens as a pre-request hook."""
        if token := (s := session).get('google_oauth_token'):
            print("Token expiring in", token['expires_at'] - time.time())
            if time.time() >= token['expires_at']:
                del s['google_oauth_token']

    from usaon_vta_survey.routes.google import blueprint
    from usaon_vta_survey.routes.login import login_bp
    from usaon_vta_survey.routes.logout import logout_bp
    from usaon_vta_survey.routes.response import bp
    from usaon_vta_survey.routes.response.applications import application_bp
    from usaon_vta_survey.routes.response.data_products import dp_bp
    from usaon_vta_survey.routes.response.observing_systems import obs_bp
    from usaon_vta_survey.routes.response.relationships.application_societal_benefit_area import (
        application_societal_benefit_area_bp,
    )
    from usaon_vta_survey.routes.response.relationships.data_product_application import (
        data_product_application_bp,
    )
    from usaon_vta_survey.routes.response.relationships.observing_system_data_product import (
        observing_system_data_product_bp,
    )
    from usaon_vta_survey.routes.response.sbas import sba_bp
    from usaon_vta_survey.routes.root import root_bp
    from usaon_vta_survey.routes.survey import survey_bp
    from usaon_vta_survey.routes.surveys import surveys_bp
    from usaon_vta_survey.routes.user import user_bp
    from usaon_vta_survey.routes.users import users_bp

    app.register_blueprint(root_bp)
    app.register_blueprint(surveys_bp)
    app.register_blueprint(survey_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(logout_bp)
    app.register_blueprint(blueprint, url_prefix="/google_oauth")
    app.register_blueprint(bp)
    app.register_blueprint(obs_bp)
    app.register_blueprint(sba_bp)
    app.register_blueprint(application_bp)
    app.register_blueprint(dp_bp)
    app.register_blueprint(observing_system_data_product_bp)
    app.register_blueprint(data_product_application_bp)
    app.register_blueprint(application_societal_benefit_area_bp)

    app.jinja_env.globals.update(sqla_inspect=sqla_inspect, __version__=__version__)

    return app
