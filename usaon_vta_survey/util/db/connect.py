import os
from functools import cache

from flask import Flask

from usaon_vta_survey.util.envvar import envvar_is_true


@cache
def db_connstr(app: Flask) -> str:
    """Produce the correct database correction string depending on app config.

    If the app is not in production mode, use SQLite; otherwise look at envvars for
    connection info.

    TODO: Get all db connection info from _one_ envvar: USAON_VTA_DB_CONNSTR. If not
    provided, use temp path.
    """
    sqlite_db = envvar_is_true('USAON_VTA_DB_SQLITE')

    if sqlite_db:
        if not (app.config["TESTING"] or app.config["DEBUG"]):
            raise RuntimeError(
                f"Production application config detected with SQLite DB. {app.config=}"
            )
        connstr = "sqlite:////db/usaon-vta.db"
        app.logger.warning(
            f"Using a local file database for development: {connstr}."
            " You should never see this logged in production!"
        )
        return connstr
    else:
        # TODOL figure out why os.environ doesn't work here
        host = os.environ['USAON_VTA_DB_HOST']
        # host = os.getenv('USAON_VTA_DB_HOST')
        port = os.environ['USAON_VTA_DB_PORT']
        user = os.getenv('USAON_VTA_DB_USER')
        password = os.getenv('USAON_VTA_DB_PASSWORD')

        connstr = f'postgresql://{user}:{password}@{host}:{port}/usaon-vta'
        return connstr
