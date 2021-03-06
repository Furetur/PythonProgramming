import unittest

from hw2.memoize import MemoizedFunction


def function(x):
    """
    Doc string
    :param x: param
    :return: something
    """
    return x


class TestMemoize(unittest.TestCase):
    def setUp(self) -> None:
        self.invocations = 0

        def f(x):
            self.invocations += 1
            return x

        self.f = MemoizedFunction(f, 10)

    def test_not_lose_original_function_name(self):
        self.assertEqual(function.__name__, MemoizedFunction(function, 1).__name__)

    def test_not_lose_original_function_doc(self):
        self.assertEqual(function.__doc__, MemoizedFunction(function, 1).__doc__)

    def test_if_all_arguments_are_unique_should_invoke_every_time(self):
        for i in range(100):
            self.f(i)
        self.assertEqual(100, self.invocations)

    def test_should_invoke_only_once_if_all_arguments_are_the_same(self):
        for i in range(100):
            self.f(1)
        self.assertEqual(1, self.invocations)

    def test_should_never_reinvoce_if_cache_is_not_overfilled(self):
        for _ in range(3):
            for i in range(5):
                self.f(i)
        self.assertEqual(5, self.invocations)

    def test_should_reinvoce_if_cache_is_overfilled(self):
        for i in range(11):
            self.f(i)
        self.f(0)
        self.assertEqual(12, self.invocations)

    def test_treat_named_positional_args_the_same(self):
        for i in range(100):
            self.f(x=1)
        self.assertEqual(1, self.invocations)


class TestMemoizeWithKeywordArgs(unittest.TestCase):
    def setUp(self) -> None:
        self.invocations = 0

        def f(x, *, y):
            self.invocations += 1
            return x, y

        self.f = MemoizedFunction(f, 10)

    def test_if_all_arguments_are_unique_should_invoke_every_time(self):
        for i in range(100):
            self.f(i, y=i)
        self.assertEqual(100, self.invocations)

    def test_should_invoke_only_once_if_all_arguments_are_the_same(self):
        for i in range(100):
            self.f(1, y=2)
        self.assertEqual(1, self.invocations)


if __name__ == "__main__":
    unittest.main()
