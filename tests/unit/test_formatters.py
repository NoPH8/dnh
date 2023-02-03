import datetime

import pytest
from flask import Request

from app.formatters import format_datetime_with_tz


@pytest.mark.parametrize('view_args, field_value, expected', [
    ({}, datetime.datetime(2022, 1, 1, 23, 0, 0), '2022-01-01 23:00:00'),
    ({'export_type': ['csv']}, None, None),
])
def test_format_datetime_with_tz(app, mocker, monkeypatch, view_args, field_value, expected):
    m_instance = mocker.Mock(created_at=field_value)

    m_request = mocker.Mock(spec=Request)
    m_request.view_args = view_args

    monkeypatch.setattr('app.formatters.request', m_request)

    result = format_datetime_with_tz(None, None, m_instance, 'created_at')
    assert result == expected
