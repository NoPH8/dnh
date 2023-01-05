import pytest

from app.tools.uri import extract_domain, validate_domain


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
