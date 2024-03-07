import os
import time
from typing import Final

from flask import Flask, session
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from markdown import Markdown
from markupsafe import Markup
from sqlalchemy import MetaData
from sqlalchemy import inspect as sqla_inspect
from werkzeug.middleware.proxy_fix import ProxyFix

from usaon_benefit_tool.constants import repo
from usaon_benefit_tool.constants.sankey import DUMMY_NODE_ID
from usaon_benefit_tool.constants.version import VERSION
from usaon_benefit_tool.util.db.connect import db_connstr
from usaon_benefit_tool.util.envvar import envvar_is_true
from usaon_benefit_tool.util.flask_jsglue import JSGlue

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
        },
    ),
)


def create_app():
    """Create and configure the app."""
    # TODO: enable override config to test_config
    # https://flask.palletsprojects.com/en/2.3.x/tutorial/factory/

    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'youcanneverguess')
    app.config['SQLALCHEMY_DATABASE_URI'] = db_connstr(app)
    app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'cosmo'

    # Set flask-login to pass redirection URL by session. This is needed because the
    # default is to pass it in the request args (i.e. URL query string); this does not
    # survive the Google OAuth dance by flask-dance.
    app.config['USE_SESSION_FOR_NEXT'] = True

    # DEV ONLY: Disable login
    app.config['LOGIN_DISABLED'] = envvar_is_true("USAON_BENEFIT_TOOL_LOGIN_DISABLED")

    if envvar_is_true("USAON_BENEFIT_TOOL_PROXY"):
        app.wsgi_app = ProxyFix(app.wsgi_app, x_prefix=1)  # type: ignore

    db.init_app(app)

    Bootstrap5(app)
    JSGlue(app)

    login_manager = LoginManager()
    login_manager.login_view = "login.login"
    login_manager.init_app(app)

    from usaon_benefit_tool.models.tables import User

    @login_manager.user_loader
    def load_user(user_id: str) -> User:
        return User.query.get(user_id)

    # Handle standalone dev deployment without need for auth secrets
    # HACK: Always logged in as dev user when login is disabled
    if app.config["LOGIN_DISABLED"]:
        import flask_login.utils as flask_login_utils

        from usaon_benefit_tool.util.dev import DEV_USER

        flask_login_utils._get_user = lambda: DEV_USER

    @app.before_request
    def before_request():
        """Handle expired google tokens as a pre-request hook."""
        if token := (s := session).get('google_oauth_token'):
            print("Token expiring in", token['expires_at'] - time.time())
            if time.time() >= token['expires_at']:
                del s['google_oauth_token']

    from usaon_benefit_tool.routes.login import google_bp, login_bp
    from usaon_benefit_tool.routes.logout import logout_bp
    from usaon_benefit_tool.routes.assessment import assessment_bp
    from usaon_benefit_tool.routes.assessments import assessments_bp
    from usaon_benefit_tool.routes.root import root_bp

    # from usaon_benefit_tool.routes.survey.applications import application_bp
    # from usaon_benefit_tool.routes.survey.observing_systems import observing_system_bp
    # from usaon_benefit_tool.routes.survey.relationships.application_societal_benefit_area import (
    #     application_societal_benefit_area_bp,
    # )
    # from usaon_benefit_tool.routes.survey.relationships.data_product_application import (
    #     data_product_application_bp,
    # )
    # from usaon_benefit_tool.routes.survey.relationships.observing_system_data_product import (
    #     observing_system_data_product_bp,
    # )
    # from usaon_benefit_tool.routes.survey.sbas import societal_benefit_area_bp
    from usaon_benefit_tool.routes.user import user_bp
    from usaon_benefit_tool.routes.users import users_bp

    app.register_blueprint(root_bp)

    app.register_blueprint(user_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(logout_bp)
    app.register_blueprint(google_bp, url_prefix="/google_oauth")

    app.register_blueprint(projects_bp)
    app.register_blueprint(project_bp)

    # Old:
    # app.register_blueprint(observing_system_bp)
    # app.register_blueprint(societal_benefit_area_bp)
    # app.register_blueprint(application_bp)
    # app.register_blueprint(observing_system_data_product_bp)
    # app.register_blueprint(data_product_application_bp)
    # app.register_blueprint(application_societal_benefit_area_bp)

    # TODO: Consider context processors instead?
    # https://flask.palletsprojects.com/en/2.3.x/templating/#context-processors
    app.jinja_env.globals.update(
        __version__=__version__,
        sqla_inspect=sqla_inspect,
        repo_url=repo.REPO_URL,
        doc_url=repo.DOC_URL,
        discuss_url=repo.DISCUSS_URL,
        current_year=repo.CURRENT_YEAR,
        constants={
            "DUMMY_NODE_ID": DUMMY_NODE_ID,
        },
    )

    md = Markdown(extensions=['fenced_code'])
    app.jinja_env.filters.update(
        markdown=lambda txt: Markup(md.convert(txt)),
        dateformat=lambda date: date.strftime("%Y-%m-%d %H:%M%Z"),
    )

    return app
