import unittest

from hw2.memoize import freeze_dict, FrozenFunctionArguments


def make_big_list(size):
    return list(range(size))


def make_big_dict(size):
    return {f"key{i}": i for i in range(size)}


class TestFreezeDict(unittest.TestCase):
    def test_frozen_dict_is_hashable(self):
        frozen_dict = freeze_dict(make_big_dict(10))
        self.assertEqual(int, type(hash(frozen_dict)))

    def test_equal_dicts_produce_equal_frozen_dicts(self):
        dict1 = make_big_dict(100)
        dict2 = make_big_dict(100)
        self.assertEqual(freeze_dict(dict1), freeze_dict(dict2))

    def test_different_dicts_produce_not_equal_frozen_dicts(self):
        dict1 = make_big_dict(100)
        dict2 = make_big_dict(10)
        self.assertNotEqual(freeze_dict(dict1), freeze_dict(dict2))


class TestFrozenArguments(unittest.TestCase):
    def test_frozen_arguments_should_be_hashable(self):
        frozen_args = FrozenFunctionArguments.from_args(*make_big_list(10), **make_big_dict(100))
        self.assertEqual(int, type(hash(frozen_args)))

    def test_equal_args_produce_equal_frozen_args(self):
        frozen_args1 = FrozenFunctionArguments.from_args(*make_big_list(10), **make_big_dict(100))
        frozen_args2 = FrozenFunctionArguments.from_args(*make_big_list(10), **make_big_dict(100))
        self.assertEqual(frozen_args1, frozen_args2)

    def test_different_args_produce_not_equal_frozen_args(self):
        frozen_args1 = FrozenFunctionArguments.from_args(*make_big_list(10), **make_big_dict(100))
        frozen_args2 = FrozenFunctionArguments.from_args(*make_big_list(10), **make_big_dict(10))
        self.assertNotEqual(frozen_args1, frozen_args2)


if __name__ == "__main__":
    unittest.main()
