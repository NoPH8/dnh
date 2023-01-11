import pytest

from app.admin import CheckAccessMixin, IPRangeModelView, RecordModelView, admin


@pytest.fixture()
def admin_view():
    def _admin_view(admin_view_class):
        return next(x for x in admin._views if isinstance(x, admin_view_class))

    return _admin_view


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
