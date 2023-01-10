import pytest

from app.tools.network import (extract_domain, get_ip_addresses_str, is_ip_address_in_network,
                               validate_domain,
                               validate_ip_address,
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


def test_get_ip_addresses_str(mocker, monkeypatch, record):
    record = record(domain='example.com')
    m_answer = mocker.Mock(side_effect=ValueError('Network failure'))
    m_logger = mocker.Mock()

    monkeypatch.setattr('app.tools.network.dns.resolver.resolve', m_answer, raising=True)
    monkeypatch.setattr('app.tools.network.logger.exception', m_logger)

    result = get_ip_addresses_str(record)

    assert result == record.ip_addresses
    assert record.ip_addresses is None
    assert record.updated_at is None
    m_logger.assert_called()


@pytest.mark.parametrize('ip_addr, ip_range, expected', [
    ('127.0.0.1', '127.0.0.0/24', True),
    ('127.0.0.2', '127.0.0.0/30', True),
    ('127.0.0.5', '127.0.0.0/30', False),
    ('3002:0bd6:0000:0000:0000:ee00:0033:6778', '127.0.0.0/30', False),
    ('127.0.0.5', '2001:db8:abcd:0012::0/64', False),
])
def test_ip_address_in_range(ip_addr, ip_range, expected):
    result = is_ip_address_in_network(ip_addr, ip_range)

    assert result == expected


@pytest.mark.parametrize('value,expected', [
    ('example', False),
    ('example.com', True),
    ('file://example.com', False),
    ('ftp://example.com', False),
])
def test_validate_domain(value, expected):
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
