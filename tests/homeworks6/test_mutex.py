import unittest
from threading import Thread
from typing import Any

from hw6.semaphore import Mutex


class MutexTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.mutex = Mutex()

    def test_is_locked_inside_critical_block(self):
        with self.mutex:
            self.assertTrue(self.mutex.locked())

    def test_releases_after_empty_block(self):
        with self.mutex:
            pass
        self.assertFalse(self.mutex.locked())

    def test_releases_even_if_exception_is_raised(self):
        try:
            with self.mutex:
                raise ArithmeticError("Some error")
        except ArithmeticError as e:
            pass

        self.assertFalse(self.mutex.locked())


class MutexIncrementsTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.mutex = Mutex()
        self.count = 0

    def increment(self, times: int):
        for i in range(times):
            with self.mutex:
                self.count += 1

    def increment_long(self, times: int):
        with self.mutex:
            for i in range(times):
                self.count += 1

    def create_increment_thread(self, times: int) -> Thread:
        return Thread(target=lambda: self.increment(times))

    def create_long_increment_thread(self, times: int) -> Thread:
        return Thread(target=lambda: self.increment_long(times))

    def test_is_released_after_1000_increments(self):
        self.create_increment_thread(1000)
        self.assertFalse(self.mutex.locked())

    def test_correctly_works_with_2_threads_and_10_000_increments_each(self):
        thread1 = self.create_increment_thread(10_000)
        thread2 = self.create_increment_thread(10_000)
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()

        self.assertEqual(20_000, self.count)

    def test_correctly_works_with_2_threads_and_100_000_increments_each(self):
        thread1 = self.create_increment_thread(100_000)
        thread2 = self.create_increment_thread(100_000)
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()

        self.assertEqual(200_000, self.count)

    def test_correctly_works_with_4_threads_and_100_000_increments_each(self):
        threads = [self.create_increment_thread(100_000) for i in range(4)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        self.assertEqual(100_000 * 4, self.count)

    def test_long_correctly_works_with_2_threads_and_100_000_increments_each(self):
        thread1 = self.create_long_increment_thread(100_000)
        thread2 = self.create_long_increment_thread(100_000)
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()

        self.assertEqual(200_000, self.count)

    def test_long_correctly_works_with_8_threads_and_1_000_000_increments_each(self):
        threads = [self.create_long_increment_thread(1_000_000) for i in range(8)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        self.assertEqual(1_000_000 * 8, self.count)


class QueueMutexTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.mutex = Mutex()
        self.results: Any = []
        self.tasks: Any = []

    def worker(self):
        while True:
            with self.mutex:
                if len(self.tasks) > 0:
                    self.results.append(self.tasks.pop())
                else:
                    return

    def dispatch_workers(self, n):
        threads = [Thread(target=self.worker) for i in range(n)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    def test_many_workers_process_1_task(self):
        self.tasks = ["a"]
        self.dispatch_workers(4)
        self.assertEqual([], self.tasks)
        self.assertEqual(["a"], self.results)

    def test_4_workers_4_tasks(self):
        self.tasks = list(range(4))
        self.dispatch_workers(4)
        self.assertEqual([], self.tasks)
        self.assertEqual(set(range(4)), set(self.results))

    def test_1_worker_processes_100_000_tasks(self):
        self.tasks = list(range(100_000))
        self.dispatch_workers(1)
        self.assertEqual([], self.tasks)
        self.assertEqual(set(range(100_000)), set(self.results))

    def test_4_workers_process_1_000_000_tasks(self):
        self.tasks = list(range(1_000_000))
        self.dispatch_workers(4)
        self.assertEqual([], self.tasks)
        self.assertEqual(set(range(1_000_000)), set(self.results))


if __name__ == "__main__":
    unittest.main()
