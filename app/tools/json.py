from datetime import date

from flask.json.provider import DefaultJSONProvider, _default


def custom_default(o):
    return o.isoformat() if isinstance(o, date) else _default(o)


class JSONProvider(DefaultJSONProvider):
    def dumps(self, obj, **kwargs) -> str:
        kwargs['default'] = custom_default
        return super().dumps(obj, **kwargs)
