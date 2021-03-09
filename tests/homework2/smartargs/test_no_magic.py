import unittest

from hw2.smart_args.smart_args_decorator import smart_args


def func_with_doc():
    """
    Doc
    """
    pass


class SmartArgsWithNoMagicTests(unittest.TestCase):
    def test_should_remain_doc_string(self):
        f = smart_args(func_with_doc)
        self.assertEqual(func_with_doc.__doc__, f.__doc__)

    def test_should_remain_function_name(self):
        f = smart_args(func_with_doc)
        self.assertEqual(func_with_doc.__name__, f.__name__)

    def test_should_work_for_functions_of_0_arity(self):
        @smart_args
        def f():
            return 1

        self.assertEqual(1, f())

    def test_should_work_for_functions_with_several_positional_arguments(self):
        @smart_args
        def f(x, y):
            return x + y

        self.assertEqual(12, f(10, 2))

    def test_should_work_for_functions_with_varargs(self):
        @smart_args
        def f(x, *args):
            return x + sum(args)

        self.assertEqual(15, f(1, 2, 3, 4, 5))

    def test_should_word_for_functions_with_positional_defaults_without_kwargs(self):
        @smart_args
        def f(x, y=1):
            return x + y

        self.assertEqual(2, f(1))

    def test_should_work_for_functions_without_positional_args_but_with_kwargs_without_defaults(self):
        @smart_args
        def f(*, x, y):
            return x + y

        self.assertEqual(3, f(x=1, y=2))

    def test_should_work_for_functions_without_positional_args_but_with_kwargs_with_non_magic_defaults(self):
        @smart_args
        def f(*, x, y=1):
            return x + y

        self.assertEqual(2, f(x=1))

    def test_should_work_for_function_with_kwargs(self):
        @smart_args
        def f(**kwargs):
            return kwargs

        self.assertEqual({"a": 1}, f(a=1))

    def test_should_work_for_any_kind_of_non_magic_argument(self):
        @smart_args
        def f(x, *args, z, w=10, **kwargs):
            return x + sum(args) + z + w + sum(kwargs.values())

        self.assertEqual(26, f(1, 2, z=3, k=10))


if __name__ == "__main__":
    unittest.main()
