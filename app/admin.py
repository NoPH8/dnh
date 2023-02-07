from typing import Iterable, Optional

import flask_admin
from flask import current_app, redirect, url_for
from flask_admin import AdminIndexView, expose
from flask_admin.actions import action
from flask_admin.contrib.sqla import ModelView
from flask_principal import PermissionDenied
from flask_security import current_user
from wtforms import PasswordField, ValidationError

from config import AppConfig

from .dashboard import dashboard
from .database import db
from .formatters import format_datetime_with_tz
from .models import APIKey, IPRange, Record, User
from .permissions import access_to_api_keys, access_to_records, access_to_users
from .tools.datetime import apply_timezone
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

    def _handle_view(self, *args, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('security.login'))


class TimeZoneMixin:
    datetime_fields: Optional[Iterable] = None
    column_formatters: dict

    def __init__(self, *args, **kwargs):
        self.datetime_fields = self.datetime_fields or []

        for field_name in self.datetime_fields:
            self.column_formatters[field_name] = format_datetime_with_tz

        super().__init__(*args, **kwargs)

    def create_form(self, obj=None):
        form = super().create_form(obj)

        return self.apply_tz_to_form_data(form)

    def edit_form(self, obj):
        form = super().edit_form(obj)

        return self.apply_tz_to_form_data(form)

    def apply_tz_to_form_data(self, form):
        for field_name in self.datetime_fields:
            if field := getattr(form, field_name, None):
                if field.data:
                    field.data = apply_timezone(
                        field.data,
                        current_app.config['SERVER_TIMEZONE'],
                        current_app.config['USER_TIMEZONE'],
                    )

        return form

    def on_model_change(self, form, instance, is_created):
        for field_name in self.datetime_fields:
            if field := getattr(form, field_name, None):
                if local_time := field.data:
                    utc_time = apply_timezone(
                        local_time,
                        current_app.config['USER_TIMEZONE'],
                        current_app.config['SERVER_TIMEZONE'],
                    )
                    setattr(instance, field_name, utc_time)


class BaseModelView(CheckAccessMixin, TimeZoneMixin, ModelView):
    pass


class UserModelView(BaseModelView):
    column_list = [
        'active',
        'username',
        'roles',
        'created_at',
        'last_login_at',
    ]

    datetime_fields = (
        'created_at',
        'last_login_at',
    )

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

    def on_model_change(self, form, instance, is_created):
        super().on_model_change(form, instance, is_created)

        raw_password = form.raw_password.data
        if is_created and not raw_password:
            raise ValidationError('Password is required for creating')
        elif form.raw_password.data:
            instance.set_password(form.raw_password.data)

    @staticmethod
    def get_access_permission():
        return access_to_users


class RecordModelView(BaseModelView):
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

    datetime_fields = (
        'created_at',
        'updated_at',
    )

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

    def on_model_change(self, form, instance, is_created):
        super().on_model_change(form, instance, is_created)

        instance.ip_addresses = None
        instance.updated_at = None
        instance.update_ip_addresses()

    @action('activate_records', 'Activate', 'Selected records will be activated')
    def activate(self, selected_ids):
        change_active_status(Record, selected_ids, True)

    @action('deactivate_records', 'Deactivate', 'Selected records will be deactivated')
    def deactivate(self, selected_ids):
        change_active_status(Record, selected_ids, False)


class IPRangeModelView(BaseModelView):
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

    datetime_fields = (
        'created_at',
    )

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


class APIPKeyModelView(BaseModelView):
    column_list = [
        'name',
        'key',
        'created_at',
    ]

    datetime_fields = (
        'created_at',
    )

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


class DashboardIndexView(AdminIndexView):
    extra_js = [
        '/static/js/admin/jquery.timeago.min.js',
        '/static/js/admin/uptime.js',
    ]

    @expose('/clear_logs', methods=('POST', ))
    def clear_logs(self):
        dashboard.clear_logs()
        return redirect('/admin/')


app_admin = flask_admin.Admin(
    name=AppConfig.APP_NAME,
    base_template='base_custom.html',
    template_mode='bootstrap4',
    index_view=DashboardIndexView(),
)
app_admin.add_view(UserModelView(User, db.session))
app_admin.add_view(RecordModelView(Record, db.session))
app_admin.add_view(IPRangeModelView(IPRange, db.session, name='IP range'))
app_admin.add_view(APIPKeyModelView(APIKey, db.session, name='API keys'))
