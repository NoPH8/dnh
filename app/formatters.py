from flask import current_app, request

from app.tools.datetime import apply_timezone


def format_datetime_with_tz(view, context, instance, field_name):
    field = getattr(instance, field_name, None)

    if 'export_type' in request.view_args:
        return field

    return (
        apply_timezone(
            field,
            current_app.config['SERVER_TIMEZONE'],
            current_app.config['USER_TIMEZONE'],
        )
        .strftime(current_app.config['DATETIME_FORMAT'])
    ) if field else field
