import pytest

from app.tools.network import (extract_domain, validate_domain, validate_ip_address,
                               validate_ip_range)


@pytest.mark.parametrize('value,expected', [
    ('example', None),
    ('example.com', None),
    ('file://example.com', None),
    ('ftp://example.com', 'example.com'),
    ('ftp://example.com/some-resource/', 'example.com'),
    ('ftp://ftp.example.com', 'ftp.example.com'),
    ('ftps://example.com', 'example.com'),
    ('http://127.0.0.1', None),
    ('http://example.com', 'example.com'),
    ('http://google', None),
    ('http://localhost', None),
    ('https://example.com', 'example.com'),
])
def test_extract_domain(value, expected):
    assert extract_domain(value) == expected


@pytest.mark.parametrize('value,expected', [
    ('example', False),
    ('example.com', True),
    ('file://example.com', False),
    ('ftp://example.com', False),
])
def test_domain_validator(value, expected):
    assert validate_domain(value) == expected


@pytest.mark.parametrize('value,expected', [
    ('127.0.0.1', True),
    ('127.0.0.258', False),
    ('127.0.0.258', False),
    ('3002:0bd6:0000:0000:0000:ee00:0033:6778', True),
    ('3002:0bd6:0000:0000:0000:ee00:0033:6778:0000', False),
    ('3002:0bd6:0000:0000:0000:ee00:0033', False),
])
def test_validate_ip_address(value, expected):
    assert validate_ip_address(value) == expected


@pytest.mark.parametrize('value,expected', [
    ('127.0.0.1/32', True),
    ('127.0.0.1/24', False),
    ('127.0.0.1', True),
    ('127.0.0.258/32', False),
    ('3002:0bd6:0000:0000:0000:ee00:0033:6778', True),
    ('3002:0bd6:0000:0000:0000:ee00:0033:6778/64', False),
    ('2001:db8:abcd:0012::0/64', True),
])
def test_validate_ip_range(value, expected):
    assert validate_ip_range(value) == expected
