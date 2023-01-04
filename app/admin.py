import flask_admin
from decouple import config
from flask import redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user

from .database import db
from .models import User


class UserModelView(ModelView):
    column_list = [
        'username',
        'role',
        'is_active',
        'last_login_at',
    ]

    form_excluded_columns = [
        'fs_uniquifier',
    ]

    form_widget_args = {
        'joined_at': {
            'disabled': True
        },
        'last_login_at': {
            'disabled': True
        },
    }

    def is_accessible(self):
        return (current_user.is_active and current_user.is_authenticated)

    def _handle_view(self, name):
        if not self.is_accessible():
            return redirect(url_for('security.login'))


admin = flask_admin.Admin(
    name=config('APP_NAME', default='DNH'),
    base_template='base_custom.html',
    template_mode='bootstrap4',
)
admin.add_view(UserModelView(User, db.session))
