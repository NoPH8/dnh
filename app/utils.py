import datetime
import uuid

import bleach

from app.constants import ROLES


def create_roles(app):
    with app.app_context():
        from .database import db

        for role_name in ROLES:
            if not app.security.datastore.find_role(role=role_name):
                app.security.datastore.create_role(name=role_name)

        db.session.commit()


def create_tables(app):
    with app.app_context():
        from .database import db
        db.create_all()


def get_fs_uniquifier():
    return uuid.uuid4().hex


def get_current_datatime():
    return datetime.datetime.now()


def uia_username_mapper(identity):
    return bleach.clean(identity, strip=True)
