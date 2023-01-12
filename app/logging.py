from collections import deque
from functools import cached_property
from logging import Formatter, StreamHandler


class FIFOTemporaryStream:
    MAX_SIZE = 30

    @cached_property
    def storage(self):
        return deque(maxlen=self.MAX_SIZE)

    def show(self):
        return iter(self.storage)

    def write(self, msg):
        self.storage.append(msg)


dashboard_format = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
dashboard_handler = StreamHandler(stream=FIFOTemporaryStream())
dashboard_handler.setFormatter(dashboard_format)
