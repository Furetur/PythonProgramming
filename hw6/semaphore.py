from threading import Lock
from types import TracebackType
from typing import Optional, Type


class Semaphore:
    def __init__(self, max_threads: int):
        self.current_threads = 0
        self.max_threads = max_threads
        self._counter_lock = Lock()

    def locked(self):
        with self._counter_lock:
            return self.current_threads == self.max_threads

    def acquire(self):
        while True:
            with self._counter_lock:
                if self.current_threads < self.max_threads:
                    self.current_threads += 1
                    break

    def release(self):
        with self._counter_lock:
            if self.current_threads >= 1:
                self.current_threads -= 1
            else:
                raise ValueError("Tried to release a free semaphore")

    def __enter__(self):
        self.acquire()

    def __exit__(self, _: Optional[Type[BaseException]], __: Optional[BaseException], ___: Optional[TracebackType]):
        self.release()


class Mutex(Semaphore):
    def __init__(self):
        super(Mutex, self).__init__(1)
