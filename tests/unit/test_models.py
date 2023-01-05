def test_user_str(user, db_session):
    instance = user()

    assert str(instance) == instance.username


def test_role_str(role, db_session):
    instance = role()

    assert str(instance) == instance.name


def test_record_str(record, db_session):
    instance = record()

    assert str(instance) == instance.domain
