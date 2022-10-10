# isort: skip_file
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData


db = SQLAlchemy(
    metadata=MetaData(naming_convention={
        'ix': 'ix_%(column_0_label)s',
        'uq': 'uq_%(table_name)s_%(column_0_name)s',
        'ck': 'ck_%(table_name)s_%(constraint_name)s',
        'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
        'pk': 'pk_%(table_name)s'
    })
)

app = Flask(__name__)
# TODO: Postgres
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db.init_app(app)

# NOTE: This is a circular import, but it's specified by the Flask docs:
#     https://flask.palletsprojects.com/en/3.1.x/patterns/packages/
import usaon_vta_survey.routes.root  # noqa: E402
