import dataclasses
import datetime
from functools import cached_property

import humanize
from flask import current_app

from app.logging import FIFOTemporaryStream


@dataclasses.dataclass()
class Dashboard:
    started = datetime.datetime.now()

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
    def uptime(self):
        return humanize.naturaldelta(datetime.datetime.now() - self.started)
