import pytest

from app import User, create_app
from app.database import db
from config import AppConfigTesting


@pytest.fixture()
def app():
    app = create_app(AppConfigTesting)

    yield app

    # clean up / reset resources here
    with app.app_context():
        db.session.remove()
        db.drop_all()

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
def user(app):
    def _user(**values) -> 'User':
        with app.app_context():
            password = values.pop('password', 'SecretPassword')
            default_values = {
                'username': 'admin',
            }

            user = app.security.datastore.create_user(**default_values | values)
            user.set_password(password)

            db.session.commit()

        return user

    return _user
