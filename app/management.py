import getpass

from flask import Blueprint, current_app
from flask_security import hash_password

from app import Role

manage_bp = Blueprint('manage', __name__)


@manage_bp.cli.command('createsuperuser')
def create_superuser_command():
    with current_app.app_context():
        from .database import db

        while True:
            username = input('Username: ')
            if current_app.security.datastore.find_user(username=username):
                print('User already exists. Set another user name')
                continue
            break

        while True:
            raw_password_1 = getpass.getpass('Password: ')
            raw_password_2 = getpass.getpass('Password (again): ')

            if raw_password_1 != raw_password_2:
                print('Passwords do not match')
            elif not raw_password_1:
                print('Empty passwords are not allowed')
            else:
                break

        current_app.security.datastore.create_user(
            username=username,
            password=hash_password(raw_password_1),
            roles=list(db.session.execute(db.select(Role)).scalars())
        )
        db.session.commit()
        print('Superuser created successfully')
