from collections import OrderedDict, namedtuple
from dataclasses import dataclass
from functools import update_wrapper


class Cache:
    def __init__(self, size):
        self.size = size
        self.data = OrderedDict()

    def __setitem__(self, key, value):
        self.data[key] = value
        if len(self.data) == self.size:
            self.data.popitem(last=False)

    def __getitem__(self, key):
        return self.data[key]

    def __contains__(self, item):
        return item in self.data


def freeze_dict(dictionary: dict):
    generic_type = namedtuple("FrozenDict", dictionary.keys())
    return generic_type(**dictionary)


@dataclass(frozen=True)
class FrozenFunctionArguments:
    args: tuple
    kwargs: namedtuple

    @staticmethod
    def from_args(*args, **kwargs):
        return FrozenFunctionArguments(args, freeze_dict(kwargs))


class MemoizedFunction:
    def __init__(self, function, cache_size, make_cache=Cache):
        self.function = function
        self.cache = make_cache(cache_size)
        update_wrapper(self, function)

    def __call__(self, *args, **kwargs):
        frozen_args = FrozenFunctionArguments.from_args(*args, **kwargs)
        if frozen_args in self.cache:
            print(f"Getting from cache {frozen_args}")
            return self.cache[frozen_args]
        else:
            print(f"Calculating {frozen_args}")
            result = self.function(*args, **kwargs)
            self.cache[frozen_args] = result
            return result


def memoize(func=None, *, cache_size):
    if func is None:
        return lambda f: memoize(f, cache_size=cache_size)

    return MemoizedFunction(func, cache_size)
