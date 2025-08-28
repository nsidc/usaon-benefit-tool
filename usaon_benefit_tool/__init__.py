import logging
import os
import time
from typing import Final

from flask import Flask, render_template, session
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from loguru import logger as loguru_logger
from markdown import Markdown
from markupsafe import Markup
from sqlalchemy import MetaData
from sqlalchemy import inspect as sqla_inspect
from werkzeug.middleware.proxy_fix import ProxyFix

from usaon_benefit_tool._types import NodeType, RoleName
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
    _monkeypatch()

    app = Flask(__name__)
    _setup_logging(app)
    _setup_config(app)
    _setup_proxy_support(app)

    db.init_app(app)

    Bootstrap5(app)
    JSGlue(app)

    _setup_login(app)
    _register_blueprints(app)
    _register_template_helpers(app)
    _register_custom_error_pages(app)

    return app


def _setup_logging(app) -> None:
    """Route logs from loguru to the app logger, and respect Gunicorn log-level.

    Based on: https://gist.github.com/M0r13n/0b8c62c603fdbc98361062bd9ebe8153
    """
    if "gunicorn" in os.environ.get("SERVER_SOFTWARE", ""):
        # sync the application log level with Gunicorn's log level
        gunicorn_logger = logging.getLogger('gunicorn.error')
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)
        loguru_logger.info(
            f"Detected Gunicorn server and set log level to {gunicorn_logger.level}.",
        )

    class InterceptHandler(logging.Handler):
        def emit(self, record):
            logger_opt = loguru_logger.opt(depth=6, exception=record.exc_info)
            logger_opt.log(record.levelno, record.getMessage())

    app.logger.addHandler(InterceptHandler())

    loguru_logger.debug("Logging configured.")


def _setup_config(app) -> None:
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'youcanneverguess')
    app.config['SQLALCHEMY_DATABASE_URI'] = db_connstr(app)
    app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'cosmo'

    # Set flask-login to pass redirection URL by session. This is needed because the
    # default is to pass it in the request args (i.e. URL query string); this does not
    # survive the Google OAuth dance by flask-dance.
    app.config['USE_SESSION_FOR_NEXT'] = True

    # DEV ONLY: Disable login
    app.config['LOGIN_DISABLED'] = envvar_is_true("USAON_BENEFIT_TOOL_LOGIN_DISABLED")

    loguru_logger.debug("App configuration initialized.")


def _setup_proxy_support(app) -> None:
    if envvar_is_true("USAON_BENEFIT_TOOL_PROXY"):
        app.wsgi_app = ProxyFix(app.wsgi_app, x_prefix=1)  # type: ignore


def _setup_login(app) -> None:
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

        flask_login_utils._get_user = lambda: User.query.get(DEV_USER.id)

    @app.before_request
    def before_request():
        """Handle expired google tokens as a pre-request hook."""
        if token := (s := session).get('google_oauth_token'):
            print("Token expiring in", token['expires_at'] - time.time())
            if time.time() >= token['expires_at']:
                del s['google_oauth_token']

    loguru_logger.debug("Login configured.")


def _register_template_helpers(app) -> None:
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
        types={
            "RoleName": RoleName,
            "NodeType": NodeType,
        },
    )

    md = Markdown(extensions=['fenced_code', 'tables'])
    app.jinja_env.filters.update(
        markdown=lambda txt: Markup(md.convert(txt)),
        dateformat=lambda date: date.strftime("%Y-%m-%d %H:%M%Z"),
    )

    loguru_logger.debug("Template helpers registered.")


def _register_blueprints(app) -> None:
    # TODO: Extract function register_blueprints
    from usaon_benefit_tool.routes.assessment import assessment_bp
    from usaon_benefit_tool.routes.assessments import assessments_bp
    from usaon_benefit_tool.routes.legend import legend_bp
    from usaon_benefit_tool.routes.login import google_bp, login_bp
    from usaon_benefit_tool.routes.logout import logout_bp
    from usaon_benefit_tool.routes.node import node_bp
    from usaon_benefit_tool.routes.nodes import nodes_bp
    from usaon_benefit_tool.routes.root import root_bp
    from usaon_benefit_tool.routes.support import support_bp
    from usaon_benefit_tool.routes.user import user_bp
    from usaon_benefit_tool.routes.users import users_bp

    app.register_blueprint(root_bp)
    app.register_blueprint(legend_bp)

    app.register_blueprint(user_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(logout_bp)
    app.register_blueprint(google_bp, url_prefix="/google_oauth")

    app.register_blueprint(assessments_bp)
    app.register_blueprint(assessment_bp)

    app.register_blueprint(nodes_bp)
    app.register_blueprint(node_bp)

    app.register_blueprint(support_bp)

    loguru_logger.debug("Blueprints registered.")


def _register_custom_error_pages(app) -> None:
    for error_code in [403, 404]:
        app.register_error_handler(
            error_code,
            lambda e, error_code=error_code: (
                render_template(f'{error_code}.html', error=e),
                error_code,
            ),
        )

    loguru_logger.debug("Custom error pages registered.")


def _monkeypatch():
    import wtforms_sqlalchemy

    from usaon_benefit_tool.util.monkeypatch.wtforms_sqlalchemy import model_fields

    wtforms_sqlalchemy.orm.model_fields = model_fields
