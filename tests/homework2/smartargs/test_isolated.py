import unittest

from hw2.smart_args.smart_args_decorator import smart_args
from hw2.smart_args.supported_magic_args import Isolated


def make_deep_dict(depth):
    dict = {}
    cur_node = dict
    for _ in range(depth):
        cur_node["a"] = {}
        cur_node = cur_node["a"]
    cur_node["a"] = 1
    return dict


def edit_deep_dict(dictionary):
    cur_node = dictionary
    while "a" in cur_node and type(cur_node["a"]) is dict:
        cur_node = cur_node["a"]
    cur_node["a"] = 2


class IsolatedTest(unittest.TestCase):
    def test_isolated_raises_if_passed_as_a_positional_argument(self):
        with self.assertRaises(TypeError):

            @smart_args
            def f(x=Isolated()):
                pass

    def test_isolated_at_least_shallow_copies(self):
        mutable = {"a": 1}

        @smart_args
        def f(*, x=Isolated()):
            x["a"] = 2
            return x

        f(x=mutable)
        self.assertEqual({"a": 1}, mutable)

    def test_isolated_deep_copies(self):
        mutable = {"a": {"b": 1}}

        @smart_args
        def f(*, x=Isolated()):
            x["a"]["b"] = 2
            return x

        f(x=mutable)
        self.assertEqual({"a": {"b": 1}}, mutable)

    def test_isolated_deep_copies_big(self):
        dic = make_deep_dict(100)

        @smart_args
        def f(*, x=Isolated()):
            edit_deep_dict(x)

        f(x=dic)
        self.assertEqual(make_deep_dict(100), dic)

    def test_isolated_raises_if_no_arg_is_passed(self):
        @smart_args
        def f(*, x=Isolated()):
            pass

        with self.assertRaises(TypeError):
            f()


if __name__ == "__main__":
    unittest.main()
