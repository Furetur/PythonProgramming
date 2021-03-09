from functools import wraps, update_wrapper

from typing import Callable, TypeVar


R = TypeVar("R")


def __curry_internal(func: Callable[..., R], arity: int, passed_args: list = None) -> Callable:
    """
    For internal use by curry_explicit only!
    """
    if passed_args is None:
        passed_args = []

    if arity < 0:
        raise TypeError(f"Arity should be non-negative but received {arity}")
    elif arity == 0:
        return update_wrapper(lambda: func(), func)

    @wraps(func)
    def curried_function(x):
        if len(passed_args) + 1 < arity:
            return __curry_internal(func, arity, [*passed_args, x])
        else:
            return func(*passed_args, x)

    return curried_function


def curry_explicit(func: Callable[..., R], arity: int) -> Callable:
    """
    Curries a function. Converts function with given arity = n into a series of n nested functions.
    If arity is 0 then returns lambda: func()
    :param func: The original function
    :param arity: Arity of the original function. Should be exactly equal to a number of positional arguments that
    the function receives if it does not accept varargs, otherwise should not be greater than the number of
    positional arguments.
    :return: A curried function.
    """
    return __curry_internal(func, arity)
