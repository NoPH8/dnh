import pytest
from flask_security import hash_password

from app import Role, User, create_app
from app.database import db
from app.models import Record
from config import AppConfigTesting


@pytest.fixture
def app():
    app = create_app(AppConfigTesting)

    with app.app_context():
        db.create_all()

        yield app

        db.session.remove()
        db.drop_all()
        # Fix for Flask-security from singleton
        delattr(app.security.confirm_register_form, 'username')
        delattr(app.security.login_form, 'username')
        delattr(app.security.register_form, 'username')


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def db_session(app):
    return db.session()


def create_instance(db_session, model_name, values: dict):
    instance = model_name(**values)
    db_session.add(instance)
    db_session.commit()

    return instance


@pytest.fixture()
def user(db_session):
    def _user(**values) -> 'User':
        password = values.pop('password', 'SecretPassword')
        users_count = db.session.query(User.id).count()

        default_values = {
            'username': f'user{users_count}',
            'password': hash_password(password),
            'roles': list(db.session.execute(db.select(Role)).scalars())
        }

        return create_instance(db_session, User, default_values | values)

    return _user


@pytest.fixture()
def role(db_session):
    def _role(**values) -> 'Role':
        roles_count = db.session.query(Role.id).count()

        default_values = {
            'name': f'role_{roles_count}',
        }

        return create_instance(db_session, Role, default_values | values)

    return _role


@pytest.fixture()
def record(db_session):
    def _record(**values) -> 'Record':
        records_count = db.session.query(Record.id).count()

        default_values = {
            'domain': f'record{records_count}.example.com',
        }

        return create_instance(db_session, Record, default_values | values)

    return _record
