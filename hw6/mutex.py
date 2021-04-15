from threading import Lock
from types import TracebackType
from typing import Optional, Type


class Mutex:
    def __init__(self):
        self.lock = Lock()

    def locked(self):
        return self.lock.locked()

    def __enter__(self):
        self.lock.acquire()

    def __exit__(self, _: Optional[Type[BaseException]], __: Optional[BaseException], ___: Optional[TracebackType]):
        self.lock.release()
