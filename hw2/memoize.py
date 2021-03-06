from collections import OrderedDict
from dataclasses import dataclass
from functools import update_wrapper
from typing import Hashable, Generic, TypeVar, Protocol, Callable, OrderedDict as OrderedDictType, Tuple, Dict

K = TypeVar("K", bound=Hashable)

V = TypeVar("V")


class Cache(Generic[K, V]):
    def __init__(self, size: int):
        """
        Cache is a KV-storage, that stores only a fixed number of KV-pairs. Implements FIFO.
        :param size: the number of KV-pairs to store
        """
        self.size = size
        self.data: OrderedDictType[K, V] = OrderedDict()

    def __setitem__(self, key: K, value: V) -> None:
        """
        Put a KV-pair into storage
        """
        self.data[key] = value
        if len(self.data) >= self.size:
            self.data.popitem(last=False)

    def __getitem__(self, key: K) -> V:
        """
        Get a value from storage
        """
        return self.data[key]

    def __contains__(self, key: K) -> bool:
        """
        Check whether the key is in the storage
        """
        return key in self.data


def freeze_dict(dictionary: Dict[K, V]) -> Tuple[Tuple[K, V], ...]:
    """
    Converts a dict into tuple of KV-pairs
    """
    return tuple((k, v) for k, v in dictionary.items())


@dataclass(frozen=True)
class FrozenFunctionArguments:
    """
    Hashable type that stores hashable function arguments of any kind.
    """

    args: Tuple[Hashable, ...]
    kwargs: Tuple[Hashable, ...]

    @staticmethod
    def from_args(*args: Hashable, **kwargs: Hashable) -> "FrozenFunctionArguments":
        """
        Converts passed arguments and keyword arguments into FrozenFunctionArguments
        """
        return FrozenFunctionArguments(args, freeze_dict(kwargs))


R = TypeVar("R", covariant=True)


class MemoizableFunction(Protocol[R]):
    """
    Function that can be memoized.
    """

    def __call__(self, *args: Hashable, **kwargs: Hashable) -> R:
        ...


class MemoizedFunction(Generic[R]):
    def __init__(self, function: MemoizableFunction[R], cache_size: int):
        self.function = function
        self.cache: Cache[Hashable, R] = Cache(cache_size)
        update_wrapper(self, function)

    def __call__(self, *args: Hashable, **kwargs: Hashable) -> R:
        frozen_args = FrozenFunctionArguments.from_args(*args, **kwargs)
        if frozen_args in self.cache:
            return self.cache[frozen_args]
        else:
            result = self.function(*args, **kwargs)
            self.cache[frozen_args] = result
            return result


def memoize(func: MemoizableFunction = None, *, cache_size: int = 0) -> Callable:
    """
    Memoizes a function. Stores only a number [cache_size] last function
    :param func: function to be memoized
    :param cache_size: the number of function (input, output) pairs to remember
    :return: memoized function
    """
    if func is None:
        return lambda f: memoize(f, cache_size=cache_size)

    return MemoizedFunction(func, cache_size)
