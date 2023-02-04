import datetime
from http import HTTPStatus

import pytest

from app.api.v1.views import get_ip_list_response
from app.constants import IP_FAMILY_VALUES

updated_at = datetime.datetime.now()


@pytest.mark.parametrize('query,expected_code,expected_json', [
    (
        '?api_key=1234567890',
        HTTPStatus.OK,
        {
            'ip_addresses': [
                '127.0.0.1',
                '127.0.1.0/24',
            ],
            'updated_at': updated_at.isoformat()
        }
    ),
    (
        '',
        HTTPStatus.UNAUTHORIZED,
        {'message': 'Please provide an API key'}
    ),
    (
        '?api_key=0987654321',
        HTTPStatus.BAD_REQUEST,
        {'message': 'The provided API key is not valid'}
    ),
    (
        '?api_key=1234567890&family=ipv8',
        HTTPStatus.BAD_REQUEST,
        {'message': f'Invalid family value. Allowed are {", ".join(IP_FAMILY_VALUES)}'}
    ),
])
def test_ip_list(client, api_key, ip_range, record, query, expected_code, expected_json):
    api_key(key='1234567890')
    record(domain='s1.example.com', ip_addresses='127.0.0.1', updated_at=updated_at)
    record(domain='s2.example.com', ip_addresses='127.0.1.1', updated_at=updated_at)
    ip_range(ip_range='127.0.1.0/24')

    result = client.get(f'/api/v1/ip_list{query}')

    assert result.status_code == expected_code
    assert result.json == expected_json


@pytest.mark.parametrize('ip_family,expected', [
    (
        'ipv4',
        {
            'ip_addresses': ['127.0.0.1'],
            'updated_at': datetime.datetime(2022, 1, 1, 23, 0, 0),
        }
    ),
    (
        'ipv6',
        {
            'ip_addresses': ['::1'],
            'updated_at': datetime.datetime(2022, 1, 1, 23, 0, 0),
        }
    ),
    (
        '',
        {
            'ip_addresses': ['127.0.0.1', '::1'],
            'updated_at': datetime.datetime(2022, 1, 1, 23, 0, 0),
        }
    ),
])
def test_get_ip_list_response(app, record, ip_family, expected):
    record(
        domain='example.com',
        ip_addresses='127.0.0.1; ::1',
        updated_at=datetime.datetime(2022, 1, 1, 23, 0, 0),
    )
    result = get_ip_list_response(ip_family)

    assert result == expected
