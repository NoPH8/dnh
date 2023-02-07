def test_has_logs(dashboard, logger_record):
    assert dashboard.has_logs


def test_clear_logs(dashboard, logger_record):
    dashboard.clear_logs()
    assert dashboard.has_logs is False
