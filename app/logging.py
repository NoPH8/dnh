import datetime
import zoneinfo
from collections import deque
from functools import cached_property
from logging import Formatter, StreamHandler


class DashboardFIFOStream:
    MAX_SIZE = 30

    @cached_property
    def dashboard(self):
        from app.dashboard import dashboard

        return dashboard

    @cached_property
    def storage(self):
        return deque(maxlen=self.MAX_SIZE)

    def clear(self):
        self.storage.clear()

    def show(self):
        return iter(self.storage)

    def write(self, msg):
        self.storage.append(msg)
        self.dashboard.update_dashboard()


class TZFormatter(Formatter):
    """override logging.Formatter to use an aware datetime object"""

    @cached_property
    def timezone(self):
        from flask import current_app

        return zoneinfo.ZoneInfo(current_app.config['USER_TIMEZONE'])

    def converter(self, timestamp):
        return datetime.datetime.fromtimestamp(timestamp, tz=self.timezone)

    def formatTime(self, record, datefmt=None):
        dt = self.converter(record.created)
        return dt.strftime(datefmt) if datefmt else dt.isoformat()


dashboard_format = TZFormatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
dashboard_handler = StreamHandler(stream=DashboardFIFOStream())
dashboard_handler.setFormatter(dashboard_format)
