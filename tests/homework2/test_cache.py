import unittest

from hw2.memoize import Cache


class TestCache(unittest.TestCase):
    def test_cache_stores_one_value(self):
        cache = Cache(4)
        cache[1] = 2
        self.assertEqual(2, cache[1])

    def test_cache_stores_last_n_values(self):
        cache = Cache(10)
        for i in range(100):
            cache[i] = i
        expected_values = set(range(90, 100))
        actual_values = set()
        for i in range(100):
            if i in cache:
                actual_values.add(i)
        self.assertTrue(expected_values, actual_values)


if __name__ == "__main__":
    unittest.main()
