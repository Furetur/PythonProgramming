import unittest

from hw2.curry import curry_explicit


def add(x: float, y: float) -> float:
    """
    Adds x + y
    :param x: first operand
    :param y: second operand
    :return: addition result
    """
    return x + y


def add_many(first, *rest):
    return sum([first, *rest])


def constant():
    return 1


def mul_with_default(x, y=1):
    return x * y


def mul_with_kwargs(x, y, *, twice=False):
    if twice:
        return 2 * x * y
    else:
        return x * y


class TestCurry(unittest.TestCase):
    def setUp(self) -> None:
        self.curried_add = curry_explicit(add, 2)

    def test_not_lose_original_function_name(self):
        self.assertEqual(add.__name__, self.curried_add.__name__)

    def test_not_lose_original_function_doc(self):
        self.assertEqual(add.__doc__, self.curried_add.__doc__)

    def test_add_should_return_a_function_when_passed_one_argument(self):
        self.assertTrue(callable(self.curried_add(1)))

    def test_passing_params_should_always_return_a_new_curried_function(self):
        self.curried_add(1)
        self.assertTrue(callable(self.curried_add(2)))

    def test_providing_negative_arity_should_raise(self):
        with self.assertRaises(TypeError):
            curry_explicit(add, -1)

    def test_add_many_should_work_with_3_arity(self):
        cur_add_many = curry_explicit(add_many, 3)
        self.assertEqual(cur_add_many(1)(2)(3), 6)

    def test_works_with_arity_0(self):
        cur_const = curry_explicit(constant, 0)
        self.assertEqual(cur_const(), 1)

    def test_should_raise_if_argument_not_provided_even_if_it_has_default_value(self):
        mul = curry_explicit(mul_with_default, 2)
        mulmul = mul(7)
        with self.assertRaises(TypeError):
            mulmul()

    def test_should_ignore_default_args(self):
        mul = curry_explicit(mul_with_default, 2)
        self.assertEqual(mul(2)(3), 6)

    def test_should_ignore_kwargs(self):
        mul = curry_explicit(mul_with_kwargs, 2)
        self.assertEqual(mul(2)(3), 6)


if __name__ == "__main__":
    unittest.main()
