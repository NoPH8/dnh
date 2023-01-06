def test_user_str(user):
    instance = user()

    assert str(instance) == instance.username


def test_role_str(role):
    instance = role()

    assert str(instance) == instance.name


def test_record_str(record):
    instance = record()

    assert str(instance) == instance.domain
