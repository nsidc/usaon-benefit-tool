import os
from functools import cache

from flask import Flask

from usaon_benefit_tool.util.envvar import envvar_is_true


@cache
def db_connstr(app: Flask) -> str:
    """Produce the correct database correction string depending on app config.

    If the app is not in production mode, use SQLite; otherwise look at envvars for
    connection info.

    If a non-production app config is detected with SQLite db, this function will throw
    an error to prevent an improper deployment.

    TODO: Get all db connection info from _one_ envvar: USAON_BENEFIT_TOOL_DB_CONNSTR.
    If not provided, default to local sqlite?
    """
    sqlite_db = envvar_is_true('USAON_BENEFIT_TOOL_DB_SQLITE')
    db_name = "usaon-benefit-tool"

    if sqlite_db:
        if not (app.config["TESTING"] or app.config["DEBUG"]):
            raise RuntimeError(
                f"Production application config detected with SQLite DB. {app.config=}"
            )
        db_path = f"/db/{db_name}.db"
        connstr = f"sqlite:///{db_path}"
        app.logger.warning(
            f"Using a local file database for development: {connstr}."
            " You should never see this logged in production!"
        )
        return connstr
    else:
        host = os.environ['USAON_BENEFIT_TOOL_DB_HOST']
        port = os.environ['USAON_BENEFIT_TOOL_DB_PORT']
        user = os.environ['USAON_BENEFIT_TOOL_DB_USER']
        password = os.environ['USAON_BENEFIT_TOOL_DB_PASSWORD']

        connstr = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'
        return connstr
