import datetime
from zoneinfo import ZoneInfo


def apply_timezone(
        datetime_value: datetime.datetime,
        current_tz_name: str,
        new_tz_name: str,
) -> datetime.datetime:

    current_tz = ZoneInfo(current_tz_name)
    new_tz = ZoneInfo(new_tz_name)

    return (
        datetime_value
        .replace(tzinfo=current_tz)
        .astimezone(tz=new_tz)
    )
