import datetime

from app.tasks import update_domain_ip_task


def test_update_domain_ip_task(mocker, monkeypatch, app, record):
    record_1 = record(domain='example.com')
    record_2_updated_at = datetime.datetime(2022, 1, 1, 23, 0, 0)
    record_2 = record(
        domain='test.example.com',
        ip_addresses='127.0.0.1',
        updated_at=record_2_updated_at,
    )

    m_answer = mocker.Mock(address='127.0.0.1')
    m_resolver = mocker.Mock(name='MockResolver')
    m_resolver().resolve.return_value = [m_answer]
    monkeypatch.setattr('app.tools.network.get_dns_resolver', m_resolver)

    update_domain_ip_task(app)

    assert record_1.ip_addresses == '127.0.0.1'
    assert record_1.updated_at is not None
    assert record_2.ip_addresses == '127.0.0.1'
    assert record_2.updated_at == record_2_updated_at
