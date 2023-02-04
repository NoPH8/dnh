import pytest

from app.api.v1.validators import ValidationError, validate_ip_family


@pytest.mark.parametrize('address,expected', [
    ('', None),
    ('ipv4', None),
    ('ipv6', None),
    ('ipv7', ValidationError),
])
def test_validate_ip_family(address, expected):
    if expected:
        with pytest.raises(expected):
            validate_ip_family(address)
    else:
        assert validate_ip_family(address) is None
