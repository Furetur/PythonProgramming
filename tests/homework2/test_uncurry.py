import unittest

from hw2.uncurry import uncurry_explicit


def add(x):
    """
    x + y
    :param x: value
    :return: function
    """

    def add2(y):
        return x + y

    return add2


add_three = lambda x: lambda y: lambda z: x + y + z


def constant():
    return 1


class TestUncurry(unittest.TestCase):
    def setUp(self) -> None:
        self.uncurried_add = uncurry_explicit(add, 2)

    def test_not_lose_original_function_name(self):
        self.assertEqual(add.__name__, self.uncurried_add.__name__)

    def test_not_lose_original_function_doc(self):
        self.assertEqual(add.__doc__, self.uncurried_add.__doc__)

    def test_for_binary_add(self):
        self.assertEqual(self.uncurried_add(5, 4), 9)

    def test_for_ternary_add(self):
        uncurried_add = uncurry_explicit(add_three, 3)
        self.assertEqual(uncurried_add(1, 2, 3), 6)

    def test_with_arity_of_0(self):
        const = uncurry_explicit(constant, 0)
        self.assertEqual(1, const())

    def test_raises_when_number_of_arguments_is_not_equal_to_arity(self):
        uncurried_add = uncurry_explicit(add_three, 2)
        with self.assertRaises(TypeError):
            uncurried_add(1, 2, 3)


if __name__ == "__main__":
    unittest.main()
