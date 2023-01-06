import pytest

from app.admin import CheckAccessMixin


def test_check_access_mixin_get_access_permission():
    with pytest.raises(NotImplementedError):
        mixin = CheckAccessMixin()
        mixin.get_access_permission()
