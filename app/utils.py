import datetime
import uuid

import bleach


def get_fs_uniquifier():
    return uuid.uuid4().hex


def get_current_datatime():
    return datetime.datetime.now()


def uia_username_mapper(identity):
    return bleach.clean(identity, strip=True)
