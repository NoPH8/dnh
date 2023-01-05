import pytest


@pytest.mark.parametrize('input_data,getpass_data,expected', [
    (
        ['admin', 'editor'],
        ['Su123456', 'Su123456'],
        'User already exists. Set another user name\nSuperuser created successfully\n'
    ),
    (
        ['editor'],
        ['', '', 'SecretPassword', 'SecretPassword'],
        'Empty passwords are not allowed\nSuperuser created successfully\n'
    ),
    (
        ['editor'],
        ['Secretpassword', 'SecretPassword', 'SecretPassword', 'SecretPassword'],
        'Passwords do not match\nSuperuser created successfully\n'
    ),
])
def test_createsuperuser(user, monkeypatch, runner, input_data, getpass_data, expected):
    user(username='admin')
    input_gen = iter(input_data)
    get_pass_gen = iter(getpass_data)

    def m_input(*args, **kwargs):
        return next(input_gen)

    def m_getpass(*args, **kwargs):
        return next(get_pass_gen)

    monkeypatch.setattr('builtins.input', m_input)
    monkeypatch.setattr('getpass.getpass', m_getpass)
    result = runner.invoke(args='manage createsuperuser')

    assert result.output == expected
