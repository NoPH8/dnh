import datetime

from app.tasks import update_domain_ip_task


def test_update_domain_ip_task_success(mocker, monkeypatch, app, record):
    record_1 = record(domain='example.com')
    record_2_updated_at = datetime.datetime(2022, 1, 1, 23, 0, 0)
    record_2 = record(
        domain='test.example.com',
        ip_addresses='127.0.0.1',
        updated_at=record_2_updated_at,
    )

    m_answer = mocker.Mock(address='127.0.0.1')
    monkeypatch.setattr('dns.resolver.resolve', lambda __: [m_answer])

    update_domain_ip_task(app)

    assert record_1.ip_addresses == '127.0.0.1'
    assert record_1.updated_at is not None
    assert record_2.ip_addresses == '127.0.0.1'
    assert record_2.updated_at == record_2_updated_at


def test_update_domain_ip_task_error(mocker, monkeypatch, app, record):
    record = record(domain='example.com')
    m_answer = mocker.Mock('Network failure')
    m_logger = mocker.Mock()

    monkeypatch.setattr('dns.resolver.resolve', lambda __: [m_answer], raising=True)
    monkeypatch.setattr('app.tasks.logger.exception', m_logger)

    update_domain_ip_task(app)

    assert record.ip_addresses is None
    assert record.updated_at is None
    m_logger.assert_called()
