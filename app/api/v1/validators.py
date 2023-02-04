from app.constants import IP_FAMILY_VALUES


class ValidationError(Exception):
    pass


def validate_ip_family(ip_family: str):
    if not ip_family:
        return

    if ip_family not in IP_FAMILY_VALUES:
        raise ValidationError
