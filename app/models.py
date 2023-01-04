from flask_security import RoleMixin, UserMixin

from app.database import db
from app.utils import get_fs_uniquifier


class UserRoles(db.Model):
    id = db.Column(
        db.Integer(),
        primary_key=True,
    )
    user_id = db.Column(
        'user_id',
        db.Integer(),
        db.ForeignKey('user.id'),
    )
    role_id = db.Column(
        'role_id',
        db.Integer(),
        db.ForeignKey('role.id'),
    )

    def __str__(self):
        return self.name


class User(UserMixin, db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    active = db.Column(
        db.Boolean(),
    )
    fs_uniquifier = db.Column(
        db.String(255),
        unique=True,
        nullable=False,
        default=get_fs_uniquifier,
    )
    roles = db.relationship(
        'Role',
        secondary='user_roles',
        backref=db.backref('users', lazy='dynamic'),
    )
    password = db.Column(
        db.String,
        nullable=False,
    )
    username = db.Column(
        db.String(255),
        unique=True,
        nullable=False,
    )


class Role(RoleMixin, db.Model):
    id = db.Column(
        db.Integer(),
        primary_key=True,
    )
    name = db.Column(
        db.String(80),
        unique=True,
    )
    description = db.Column(
        db.String,
        unique=True,
    )

    def __str__(self):
        return self.name
