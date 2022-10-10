# isort: skip_file
from flask import Flask

app = Flask(__name__)

# NOTE: This is a circular import, but it's specified by the Flask docs:
#     https://flask.palletsprojects.com/en/3.1.x/patterns/packages/
import usaon_vta_survey.routes.root  # noqa: E402
