import pytest

from usaon_vta_survey import app as my_app


@pytest.fixture()
def app():
    yield my_app


@pytest.fixture()
def client(app):
    return app.test_client()
