import os
from typing import Final

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy import inspect as sqla_inspect

from usaon_vta_survey.constants.db import DB_CONNSTR
from usaon_vta_survey.constants.version import VERSION

__version__: Final[str] = VERSION

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

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'youcanneverguess')
app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONNSTR

db.init_app(app)

app.jinja_env.globals.update(sqla_inspect=sqla_inspect)

# NOTE: This is a circular import, but it's specified by the Flask docs:
#     https://flask.palletsprojects.com/en/3.1.x/patterns/packages/
import usaon_vta_survey.routes  # noqa: E402, F401
