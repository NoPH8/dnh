def test_user_str(user):
    instance = user()

    assert str(instance) == instance.username


def test_role_str(role):
    instance = role()

    assert str(instance) == instance.name


def test_record(record):
    instance = record(ip_addresses='127.0.0.1')

    assert str(instance) == instance.domain


def test_ip_range(ip_range):
    instance = ip_range(ip_range='127.0.0.0/24')

    assert str(instance) == instance.ip_range


def test_api_key(api_key):
    instance = api_key()

    assert str(instance) == instance.name
