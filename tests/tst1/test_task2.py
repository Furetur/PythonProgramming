import unittest

from test1.task2 import takes


def function_with_doc(x):
    """
    Doc string
    :param x: param
    :return: something
    """
    return x


decorated_with_doc = takes(int)(function_with_doc)


class MyTestCase(unittest.TestCase):
    def test_not_lose_original_function_name(self):
        self.assertEqual(function_with_doc.__name__, decorated_with_doc.__name__)

    def test_not_lose_original_function_doc(self):
        self.assertEqual(function_with_doc.__doc__, decorated_with_doc.__doc__)

    def test_1_positional_arg_function_should_return_correct_value(self):
        @takes(int)
        def f(x):
            return x

        self.assertEqual(100, f(100))

    def test_1_positional_arg_function_should_throw_if_type_is_wrong(self):
        @takes(int)
        def f(x):
            return x

        with self.assertRaises(TypeError):
            f("1")

    def test_not_provided_positional_types_should_not_be_checked(self):
        @takes(int)
        def f(x, y):
            return x, y

        self.assertEqual((1, "a"), f(1, "a"))

    def test_should_raise_if_wrong_type_of_kwarg(self):
        @takes(x=str)
        def f(*, x):
            return x

        with self.assertRaises(TypeError):
            f(x=1)

    def test_should_raise_if_wrong_type_of_positional_arg_provided_via_kwargs(self):
        @takes(int)
        def f(x):
            return x

        with self.assertRaises(TypeError):
            f(x="a")


if __name__ == "__main__":
    unittest.main()
