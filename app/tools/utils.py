import datetime
import uuid

from app.constants import ROLES


def create_roles(app):
    with app.app_context():
        from app.database import db

        for role_name in ROLES:
            if not app.security.datastore.find_role(role=role_name):
                app.security.datastore.create_role(name=role_name)

        db.session.commit()


def create_tables(app):
    with app.app_context():
        from app.database import db
        db.create_all()


def get_unique_uuid():
    return uuid.uuid4().hex


def get_current_datatime():
    return datetime.datetime.now()
