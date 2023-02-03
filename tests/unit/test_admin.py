import datetime
from zoneinfo import ZoneInfo

import pytest

from app.admin import (CheckAccessMixin, IPRangeModelView, RecordModelView,
                       TimeZoneMixin)


def test_check_access_mixin_get_access_permission():
    with pytest.raises(NotImplementedError):
        mixin = CheckAccessMixin()
        mixin.get_access_permission()


@pytest.mark.parametrize('init_value,method_name,expected', [
    (False, 'activate', True),
    (True, 'deactivate', False),
])
def test_record_model_view_actions(admin_view, record, init_value, method_name, expected):
    instance = record(active=init_value)
    admin_view = admin_view(RecordModelView)

    getattr(admin_view, method_name)([instance.id])

    assert instance.active == expected


@pytest.mark.parametrize('init_value,method_name,expected', [
    (False, 'activate', True),
    (True, 'deactivate', False),
])
def test_ip_range_model_view_actions(admin_view, ip_range, init_value, method_name, expected):
    instance = ip_range(active=init_value)
    admin_view = admin_view(IPRangeModelView)

    getattr(admin_view, method_name)([instance.id])

    assert instance.active == expected


def test_time_zone_mixin_edit_form(app, mocker):
    current_tz = 'Europe/Kyiv'
    app.config['TIMEZONE'] = current_tz

    now = datetime.datetime.now()
    m_form = mocker.Mock()
    m_form.example.data = now

    class DummyBaseAdmin:
        column_formatters = {}

        def edit_form(self, obj):
            return m_form

    class DummyAdmin(TimeZoneMixin, DummyBaseAdmin):
        datetime_fields = ('example',)

    admin = DummyAdmin()

    admin.edit_form(mocker.Mock())
    assert m_form.example.data.tzinfo == ZoneInfo(current_tz)
