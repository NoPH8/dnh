import ipaddress


def test_user_str(user):
    instance = user()

    assert str(instance) == instance.username


def test_role_str(role):
    instance = role()

    assert str(instance) == instance.name


def test_record_str(record):
    instance = record()

    assert str(instance) == instance.domain


def test_recort_ip_address_list(record):
    instance = record(ip_addresses='127.0.0.1')

    assert instance.ip_address_list == [ipaddress.ip_address('127.0.0.1')]
