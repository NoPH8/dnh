import datetime

import pytest

from app.tools.json import custom_default

now = datetime.datetime.now()


@pytest.mark.parametrize('input_value,expected', [
    ('string', 'string'),
    (now, now.isoformat()),
])
def test_custom_default(monkeypatch, input_value, expected):
    monkeypatch.setattr('app.tools.json._default', lambda x: x)
    result = custom_default(input_value)

    assert result == expected
