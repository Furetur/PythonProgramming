import time
import unittest
from threading import Thread
from typing import List

from hw6.semaphore import Semaphore


class Worker:
    def __init__(self, semaphore):
        self.semaphore = semaphore
        self.finished = False
        self.thread = Thread(target=self.__work)

    def __work(self):
        with self.semaphore:
            self.finished = True
            time.sleep(1)

    def start(self):
        self.thread.start()

    def wait_until_finishes(self):
        self.thread.join()


class MutexTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.sem = Semaphore(2)
        self.workers: List[Worker] = []

    def dispatch_workers(self, n: int):
        self.workers = [Worker(self.sem) for i in range(n)]
        for worker in self.workers:
            worker.start()

    def wait_until_workers_finish(self):
        for worker in self.workers:
            worker.wait_until_finishes()

    def test_should_raise_if_semaphore_is_released_to_many_times(self):
        sem = Semaphore(3)
        with sem:
            pass
        with self.assertRaises(ValueError):
            sem.release()

    def test_should_let_2_threads(self):
        self.dispatch_workers(2)

        time.sleep(0.1)
        self.assertTrue(self.workers[0].finished)
        self.assertTrue(self.workers[1].finished)

        self.wait_until_workers_finish()

    def test_should_not_let_third_thread(self):
        self.dispatch_workers(3)

        time.sleep(0.1)
        self.assertFalse(self.workers[2].finished)

        self.wait_until_workers_finish()
