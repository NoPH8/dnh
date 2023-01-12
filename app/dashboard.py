import dataclasses
import datetime
from functools import cached_property
from typing import Optional

import humanize
from flask import current_app

from app.logging import FIFOTemporaryStream


@dataclasses.dataclass()
class Dashboard:
    started = datetime.datetime.now()
    _records_last_updated_at: Optional[datetime.datetime] = None

    @property
    def log(self):
        return self.log_stream.show()

    @property
    def log_length(self):
        return self.log_stream.MAX_SIZE

    @cached_property
    def log_stream(self):  # pragma: no cover
        handler = next(
            x for x in current_app.logger.handlers if isinstance(x.stream, FIFOTemporaryStream)
        )
        return handler.stream

    @property
    def records_last_updated_at(self):
        return self._records_last_updated_at.strftime('%d-%m-%Y %H:%M:%S') or 'Unknown'

    @property
    def records_next_updated_at(self):
        return (
            humanize.naturaltime(
                self._records_last_updated_at +
                datetime.timedelta(minutes=current_app.config['DNS_UPDATE_INTERVAL'])
            )
            if self._records_last_updated_at else 'Unknown'
        )

    @property
    def uptime(self):
        return humanize.naturaldelta(datetime.datetime.now() - self.started)
