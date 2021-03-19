import unittest

from test1.task1 import spy, get_usage_statistic


def function_with_doc(x, y):
    """
    Doc
    """
    return x + y


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        @spy
        def f(x, y, *, z):
            return x + y + z

        self.f = f

    def get_all_args_stats(self):
        return [(info.args, info.kwargs) for info in get_usage_statistic(self.f)]

    def test_not_lose_original_function_name(self):
        self.assertEqual(function_with_doc.__name__, spy(function_with_doc).__name__)

    def test_not_lose_original_function_doc(self):
        self.assertEqual(function_with_doc.__doc__, spy(function_with_doc).__doc__)

    def test_function_returns_the_same_values(self):
        self.assertEqual(100, self.f(50, 40, z=10))

    def test_invocation_history_is_initially_empty(self):
        stats = list(get_usage_statistic(self.f))
        self.assertEqual(0, len(stats))

    def test_after_calling_a_function_history_should_contain_only_those_params(self):
        self.f(50, 40, z=10)
        args = self.get_all_args_stats()
        expected_args = [((50, 40), {"z": 10})]
        self.assertEqual(expected_args, args)

    def test_after_calling_a_function_twice_history_should_contain_those_2_calls(self):
        self.f(50, 40, z=10)
        self.f(100, 45, z=20)
        args = self.get_all_args_stats()
        expected_args = [((50, 40), {"z": 10}), ((100, 45), {"z": 20})]
        self.assertEqual(expected_args, args)

    def test_hostory_should_contain_all_function_calls(self):
        expected_args = [((i, 100 * i), {"z": -i}) for i in range(100)]
        for i in range(100):
            self.f(i, 100 * i, z=-i)
        args = self.get_all_args_stats()
        self.assertEqual(expected_args, args)


if __name__ == "__main__":
    unittest.main()
