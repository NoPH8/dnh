from flask_security import (RoleMixin, UserMixin)
from peewee import BooleanField, CharField, DateTimeField, ForeignKeyField, TextField

from app.database import db
from app.utils import get_current_datatime, get_fs_uniquifier


class Role(RoleMixin, db.Model):
    name = CharField(unique=True)
    description = TextField(null=True)
    permissions = TextField(null=True)


class User(UserMixin, db.Model):
    active = BooleanField(default=True)
    fs_uniquifier = TextField(null=False, default=get_fs_uniquifier)
    joined_at = DateTimeField(null=True, default=get_current_datatime)
    last_login_at = DateTimeField(null=True)
    password = CharField()
    username = CharField(unique=True)


class UserRoles(db.Model):
    # Because peewee does not come with built-in many-to-many
    # relationships, we need this intermediary class to link
    # user to roles.
    user = ForeignKeyField(User, related_name='roles')
    role = ForeignKeyField(Role, related_name='users')
    name = property(lambda self: self.role.name)
    description = property(lambda self: self.role.description)

    def get_permissions(self):
        return self.role.get_permissions()
