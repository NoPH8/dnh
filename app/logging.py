import datetime
import zoneinfo
from collections import deque
from functools import cached_property
from logging import Formatter, StreamHandler

from config import AppConfig

tz = zoneinfo.ZoneInfo(AppConfig.TIMEZONE)


class FIFOTemporaryStream:
    MAX_SIZE = 30

    @cached_property
    def storage(self):
        return deque(maxlen=self.MAX_SIZE)

    def show(self):
        return iter(self.storage)

    def write(self, msg):
        self.storage.append(msg)


class TZFormatter(Formatter):
    """override logging.Formatter to use an aware datetime object"""

    @staticmethod
    def converter(timestamp):
        return datetime.datetime.fromtimestamp(timestamp, tz=tz)

    def formatTime(self, record, datefmt=None):
        dt = self.converter(record.created)
        return dt.strftime(datefmt) if datefmt else dt.isoformat()


dashboard_format = TZFormatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
dashboard_handler = StreamHandler(stream=FIFOTemporaryStream())
dashboard_handler.setFormatter(dashboard_format)
