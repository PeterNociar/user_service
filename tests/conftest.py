import os

import factory
import pytest

from config import basedir
from users import create_app
from users.models import db as _db, User

TEST_DB_PATH = f'{basedir}/test_app.db'

TEST_DATABASE_URI = f'sqlite:////{TEST_DB_PATH}'


@pytest.fixture(scope='session')
def app(request):
    """
    App fixture

    :param request:
    :return app:
    """
    settings_override = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': TEST_DATABASE_URI,
        'PRESERVE_CONTEXT_ON_EXCEPTION': False,
    }
    app = create_app(settings_override)

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope='session')
def db(app, request):
    """
    Database fixture

    :param app:
    :param request:
    :return db:
    """
    if os.path.exists(TEST_DB_PATH):
        os.unlink(TEST_DB_PATH)

    def teardown():
        _db.drop_all()
        os.unlink(TEST_DB_PATH)

    _db.app = app
    _db.create_all()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope='function')
def session(db, request):
    """
    Database session fixture

    :param db:
    :param request:
    :return session:
    """
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session


@pytest.fixture(scope='module')
def test_client(app):
    """
    Test client fixture

    :param app:
    :return:
    """
    testing_client = app.test_client()
    ctx = app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()


@pytest.fixture(scope='function')
def user_factory(session):
    """
    User factory fixture

    :param session:
    :return:
    """
    class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = User
            sqlalchemy_session = session

    return UserFactory
