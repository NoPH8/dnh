from flask_security import RoleMixin, UserMixin, hash_password

from app.database import db
from app.tools.utils import get_current_datatime, get_fs_uniquifier


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


class User(UserMixin, db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    active = db.Column(
        db.Boolean(),
        default=True,
    )
    created_at = db.Column(
        db.DateTime,
        default=get_current_datatime,
    )
    fs_uniquifier = db.Column(
        db.String(255),
        unique=True,
        default=get_fs_uniquifier,
    )
    password = db.Column(
        db.String,
        nullable=False,
    )
    last_login_at = db.Column(
        db.DateTime,
        nullable=True,
    )
    roles = db.relationship(
        'Role',
        secondary='user_roles',
        backref=db.backref('users', lazy='dynamic'),
    )
    username = db.Column(
        db.String(255),
        unique=True,
        nullable=False,
    )

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        self.password = hash_password(raw_password)


class Role(RoleMixin, db.Model):
    id = db.Column(
        db.Integer(),
        primary_key=True,
    )
    name = db.Column(
        db.String(80),
        unique=True,
    )

    def __str__(self):
        return self.name


class Record(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    created_at = db.Column(
        db.DateTime,
        default=get_current_datatime,
    )
    domain = db.Column(
        db.String,
        unique=True,
        nullable=False,
    )
    description = db.Column(
        db.String,
        nullable=True,
    )
    ip_addresses = db.Column(
        db.String,
        nullable=True,
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=True,
    )

    def __str__(self):
        return self.domain
