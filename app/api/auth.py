import functools
from http import HTTPStatus

from flask import request

from app.models import APIKey


def api_key_required(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        key_value = request.args.get('api_key')
        if key_value is None:
            return {'message': 'Please provide an API key'}, HTTPStatus.UNAUTHORIZED
        elif APIKey.find_by_key(key_value):
            return func(*args, **kwargs)
        else:
            return {'message': 'The provided API key is not valid'}, HTTPStatus.BAD_REQUEST

    return decorator
