import datetime
from http import HTTPStatus

import pytest

updated_at = datetime.datetime.now()


@pytest.mark.parametrize('query,expected_code,expected_json', [
    (
        '?api_key=1234567890',
        HTTPStatus.OK,
        {
            'ip_addresses': [
                "127.0.0.1",
                "127.0.1.0/24",
            ],
            "updated_at": updated_at.isoformat()
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
])
def test_ip_list(client, api_key, ip_range, record, query, expected_code, expected_json):
    api_key(key='1234567890')
    record(domain='s1.example.com', ip_addresses='127.0.0.1', updated_at=updated_at)
    record(domain='s2.example.com', ip_addresses='127.0.1.1', updated_at=updated_at)
    ip_range(ip_range='127.0.1.0/24')

    result = client.get(f'/api/v1/ip_list{query}')

    assert result.status_code == expected_code
    assert result.json == expected_json
