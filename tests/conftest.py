from unittest import mock

import pytest
from flask_login import FlaskLoginClient
from mock_alchemy.mocking import UnifiedAlchemyMagicMock

from usaon_vta_survey import app as my_app
from usaon_vta_survey.models.tables import User


@pytest.fixture()
def app():
    yield my_app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def session_with_user():
    session = UnifiedAlchemyMagicMock(
        data=[
            (
                [mock.call.query(User), mock.call.get(1)],
                [User(id=1, email='foo@example.com', name='foo bar', role_id='admin')],
            )
        ]
    )
    return session


@pytest.fixture()
def client_logged_in(app, session_with_user):
    app.test_client_class = FlaskLoginClient
    user = session_with_user.query(User).get(1)
    return app.test_client(user=user)
