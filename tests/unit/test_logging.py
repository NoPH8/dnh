import zoneinfo
from datetime import datetime

import pytest

from app.logging import FIFOTemporaryStream, TZFormatter


def test_fifo_temporary_stream():
    stream = FIFOTemporaryStream()
    stream.write('Test msg')

    assert list(stream.show()) == ['Test msg']


@pytest.mark.parametrize('created_dt, format_dt, expected', [
    ('2022-12-31 23:59:39+0200', None, '2022-12-31T21:59:39+00:00'),
    ('2022-12-31 23:59:39+0200', '%Y-%m-%d %H:%M:%S', '2022-12-31 21:59:39'),
])
def test_tz_formatter(mocker, monkeypatch, created_dt, format_dt, expected):
    monkeypatch.setattr('app.logging.tz', zoneinfo.ZoneInfo('UTC'))
    formatter = TZFormatter()
    created = datetime.timestamp(datetime.strptime(created_dt, '%Y-%m-%d %H:%M:%S%z'))
    record = mocker.Mock(created=created)

    result = formatter.formatTime(record, format_dt)
    assert result == expected
