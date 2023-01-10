import datetime
from http import HTTPStatus


def test_ip_list(client, record, ip_range):
    updated_at = datetime.datetime.now()
    record(domain='s1.example.com', ip_addresses='127.0.0.1', updated_at=updated_at)
    record(domain='s2.example.com', ip_addresses='127.0.1.1', updated_at=updated_at)
    ip_range(ip_range='127.0.1.0/24')

    expected = {
        'ip_addresses': [
            "127.0.0.1",
            "127.0.1.0/24",
        ],
        "updated_at": updated_at.isoformat()
    }

    result = client.get('/api/v1/ip_list')

    assert result.status_code == HTTPStatus.OK
    assert result.json == expected
