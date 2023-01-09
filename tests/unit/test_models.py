import ipaddress


def test_user_str(user):
    instance = user()

    assert str(instance) == instance.username


def test_role_str(role):
    instance = role()

    assert str(instance) == instance.name


def test_record(record):
    instance = record(ip_addresses='127.0.0.1')

    assert str(instance) == instance.domain
    assert instance.ip_address_list == [ipaddress.ip_address('127.0.0.1')]


def test_ip_range(ip_range):
    instance = ip_range(ip_range='127.0.0.0/24')

    assert str(instance) == instance.ip_range
    assert instance.ip_network == ipaddress.ip_network(instance.ip_range)
