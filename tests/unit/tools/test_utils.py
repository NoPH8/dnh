import pytest

from app import create_roles


@pytest.mark.parametrize('find_role,expected', [
    (False, True),
    (True, False),
])
def test_create_roles(mocker, monkeypatch, app, find_role, expected):
    m_find_role = mocker.Mock(return_value=find_role)
    m_create_role = mocker.Mock()
    monkeypatch.setattr(app.security.datastore, 'find_role', m_find_role)
    monkeypatch.setattr(app.security.datastore, 'create_role', m_create_role)

    create_roles(app)
    assert m_create_role.called == expected
