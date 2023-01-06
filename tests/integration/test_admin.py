from http import HTTPStatus

import pytest

from app.models import Record


def test_user_login(user, client):
    username = 'admin'
    password = 'SecretPassword'
    user(username=username, password=password)
    response = client.post('admin/login/', data={'username': username, 'password': password})

    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize('is_auth,expected', [
    (True, HTTPStatus.OK),
    (False, HTTPStatus.FOUND),
])
def test_user_list(user, client, is_auth, expected):
    user(is_auth=is_auth)
    response = client.get('admin/user/')

    assert response.status_code == expected


@pytest.mark.parametrize('password,expected,error', [
    ('SecurePassword', HTTPStatus.FOUND, ''),
    ('', HTTPStatus.OK, 'Password is required for creating'),
])
def test_user_create(user, client, password, expected, error):
    user(is_auth=True)
    response = client.post('admin/user/new/', data={'username': 'test', 'raw_password': password})

    assert response.status_code == expected
    assert error in response.text


@pytest.mark.parametrize('new_password,expected_password', [
    # ('new_password', 'new_password'),
    ('', 'old_password'),
])
def test_user_update(user, client, new_password, expected_password):
    target_user = user(password='old_password')
    user(is_auth=True)
    response = client.post(
        f'admin/user/edit/?id={target_user.id}',
        data={'username': 'test', 'raw_password': new_password})

    assert response.status_code == HTTPStatus.FOUND
    assert target_user.verify_and_update_password(expected_password)


@pytest.mark.parametrize('domain_value,expected', [
    ('https://example.com', 'example.com'),
    ('example.com', 'example.com'),
])
def test_record_create_success(db, client, user, domain_value, expected):
    user(is_auth=True)

    response = client.post('admin/record/new/', data={'domain': domain_value})

    assert response.status_code == HTTPStatus.FOUND
    record = db.session.execute(db.select(Record)).scalar()
    assert record.domain == expected


@pytest.mark.parametrize('domain_value,expected', [
    ('domain_value', 'Invalid domain name'),
    ('', 'This field is required'),
])
def test_record_create_invalid(db, client, user, domain_value, expected):
    user(is_auth=True)

    response = client.post('admin/record/new/', data={'domain': domain_value})

    assert response.status_code == HTTPStatus.OK
    assert expected in response.text


def test_record_delete(db, client, record, user):
    user(is_auth=True)
    record = record()

    response = client.post('admin/record/delete/', data={'id': record.id})

    assert response.status_code == HTTPStatus.FOUND
    assert db.session.execute(db.select(Record)).scalar() is None
