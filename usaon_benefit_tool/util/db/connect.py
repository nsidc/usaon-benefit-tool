import os
from functools import cache

from flask import Flask

from usaon_benefit_tool.util.envvar import envvar_is_true

DB_NAME = "usaon-benefit-tool"


@cache
def db_connstr(app: Flask) -> str:
    """Produce the correct database correction string depending on app config.

    If the app is not in production mode, use SQLite; otherwise look at envvars for
    connection info.

    If a non-dev app config is detected with SQLite db, this function will throw an
    error to prevent an improper deployment.

    TODO: Get all db connection info from _one_ envvar: USAON_BENEFIT_TOOL_DB_CONNSTR.
    If not provided, default to local sqlite?
    """
    sqlite_db = envvar_is_true('USAON_BENEFIT_TOOL_DB_SQLITE')

    if sqlite_db:
        return _sqlite_db_connstr(app)
    else:
        return _postgres_db_connstr()


def _postgres_db_connstr() -> str:
    host = os.environ['USAON_BENEFIT_TOOL_DB_HOST']
    port = os.environ['USAON_BENEFIT_TOOL_DB_PORT']
    user = os.environ['USAON_BENEFIT_TOOL_DB_USER']
    password = os.environ['USAON_BENEFIT_TOOL_DB_PASSWORD']

    return f'postgresql://{user}:{password}@{host}:{port}/{DB_NAME}'


def _sqlite_db_connstr(app: Flask) -> str:
    if not (app.config["TESTING"] or app.config["DEBUG"]):
        raise RuntimeError(
            f"Production application config detected with SQLite DB. {app.config=}",
        )

    connstr = f"sqlite:////db/{DB_NAME}.db"
    app.logger.warning(
        f"Using a local file database for development: {connstr}."
        " You should never see this logged in production!",
    )
    return connstr
