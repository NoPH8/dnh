import flask_admin
from decouple import config
from flask import redirect, url_for
from flask_admin.actions import action
from flask_admin.contrib.sqla import ModelView
from flask_principal import PermissionDenied
from flask_security import current_user
from wtforms import PasswordField, ValidationError

from .database import db
from .models import APIKey, IPRange, Record, User
from .permissions import access_to_api_keys, access_to_records, access_to_users
from .tools.network import extract_domain, validate_domain, validate_ip_range


def change_active_status(model, selected_ids, new_status):
    db.session.query(model).filter(model.id.in_(selected_ids)).update({'active': new_status})
    db.session.commit()


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
        'active',
        'username',
        'roles',
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
    can_export = True

    column_filters = [
        'active',
        'domain',
        'description',
        'ip_addresses',
        'created_at',
        'updated_at',
    ]

    column_list = [
        'active',
        'domain',
        'description',
        'ip_addresses',
        'created_at',
        'updated_at',
    ]

    form_columns = [
        'domain',
        'description',
        'active',
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

    def on_model_change(self, form, model, is_created):
        model.update_ip_addresses()

    @action('activate_records', 'Activate', 'Selected records will be activated')
    def activate(self, selected_ids):
        change_active_status(Record, selected_ids, True)

    @action('deactivate_records', 'Deactivate', 'Selected records will be deactivated')
    def deactivate(self, selected_ids):
        change_active_status(Record, selected_ids, False)


class IPRangeModelView(CheckAccessMixin, ModelView):
    can_export = True

    column_labels = {
        'ip_range': 'IP range'
    }

    column_filters = [
        'active',
        'ip_range',
        'description',
        'created_at',
    ]

    column_list = [
        'active',
        'ip_range',
        'description',
        'created_at',
    ]

    form_columns = [
        'active',
        'ip_range',
        'description',
        'created_at',
    ]

    form_widget_args = {
        'created_at': {
            'disabled': True,
        },
    }

    @staticmethod
    def get_access_permission():
        return access_to_records

    def validate_form(self, form):
        if hasattr(form, 'ip_range'):  # Not Delete operation
            if ip_range := form.ip_range.data:
                if not validate_ip_range(ip_range):
                    form.ip_range.errors = ('Invalid IP range', )

                    return False

        return super().validate_form(form)

    @action('activate_ip_ranges', 'Activate', 'Selected IP ranges will be activated')
    def activate(self, selected_ids):
        change_active_status(IPRange, selected_ids, True)

    @action('deactivate_ip_ranges', 'Deactivate', 'Selected IP ranges will be deactivated')
    def deactivate(self, selected_ids):
        change_active_status(IPRange, selected_ids, False)


class APIPKeyModelView(CheckAccessMixin, ModelView):
    column_list = [
        'name',
        'key',
        'created_at',
    ]

    form_columns = [
        'name',
        'key',
        'created_at',
    ]

    form_widget_args = {
        'created_at': {
            'disabled': True,
        },
        'key': {
            'disabled': True,
        },
    }

    @staticmethod
    def get_access_permission():
        return access_to_api_keys


app_admin = flask_admin.Admin(
    name=config('APP_NAME', default='DNH'),
    base_template='base_custom.html',
    template_mode='bootstrap4',
)
app_admin.add_view(UserModelView(User, db.session))
app_admin.add_view(RecordModelView(Record, db.session))
app_admin.add_view(IPRangeModelView(IPRange, db.session, name='IP range'))
app_admin.add_view(APIPKeyModelView(APIKey, db.session, name='API keys'))
