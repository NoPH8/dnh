import flask_admin
from decouple import config
from flask import redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_principal import PermissionDenied
from flask_security import current_user
from wtforms import PasswordField, ValidationError

from .database import db
from .models import Record, User
from .permissions import access_to_records, access_to_users
from .tools.uri import extract_domain, validate_domain


class CheckAccessMixin:
    def is_accessible(self):
        role_permission = self.get_access_permission()
        try:
            with role_permission.require():
                return current_user.is_active and current_user.is_authenticated
        except PermissionDenied:
            return False

    @staticmethod
    def get_access_permission():
        raise NotImplementedError('Specify permission explicitly')

    def _handle_view(self, name):
        if not self.is_accessible():
            return redirect(url_for('security.login'))


class UserModelView(CheckAccessMixin, ModelView):
    column_list = [
        'username',
        'roles',
        'is_active',
        'created_at',
        'last_login_at',
    ]

    form_excluded_columns = [
        'fs_uniquifier',
        'created_at',
        'last_login_at',
        'password',
    ]

    form_columns = [
        'username',
        'raw_password',
        'active',
        'roles',
    ]

    form_extra_fields = {
        'raw_password': PasswordField('Password')
    }

    form_widget_args = {
        'raw_password': {
            'placeholder': 'Enter new password here to change password',
        },
    }

    def on_model_change(self, form, User, is_created):
        raw_password = form.raw_password.data
        if is_created and not raw_password:
            raise ValidationError('Password is required for creating')
        elif form.raw_password.data:
            User.set_password(form.raw_password.data)

    @staticmethod
    def get_access_permission():
        return access_to_users


class RecordModelView(CheckAccessMixin, ModelView):
    column_list = [
        'domain',
        'description',
        'ip_addresses',
        'created_at',
        'updated_at',
    ]

    form_columns = [
        'domain',
        'description',
        'ip_addresses',
        'created_at',
        'updated_at',
    ]

    form_widget_args = {
        'created_at': {
            'disabled': True,
        },
        'ip_addresses': {
            'disabled': True,
        },
        'updated_at': {
            'disabled': True,
        },
    }

    @staticmethod
    def get_access_permission():
        return access_to_records

    def validate_form(self, form):
        if hasattr(form, 'domain'):  # Not Delete operation
            if domain_data := form.domain.data:
                if extracted_domain := extract_domain(domain_data):
                    form.domain.data = extracted_domain
                elif not validate_domain(domain_data):
                    form.domain.errors = ('Invalid domain name', )

                    return False

        return super().validate_form(form)


admin = flask_admin.Admin(
    name=config('APP_NAME', default='DNH'),
    base_template='base_custom.html',
    template_mode='bootstrap4',
)
admin.add_view(UserModelView(User, db.session))
admin.add_view(RecordModelView(Record, db.session))
