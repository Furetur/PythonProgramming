import inspect
from functools import wraps, update_wrapper

from typing import Callable, Any, TypeVar


def positional_arity(func: Callable[..., Any]) -> int:
    """
    Returns the number of positional arguments for func (excluding varargs).
    :param func: any function
    :return: number of positional arguments of func
    """
    args, *rest = inspect.getfullargspec(func)
    return len(args)


def has_varargs(func: Callable[..., Any]) -> bool:
    """
    :param func: any function
    :return: True if func accepts varargs else False
    """
    _, vararg, *rest = inspect.getfullargspec(func)
    return vararg is not None


R = TypeVar("R")


def __check_curry_arity(func: Callable[..., R], arity: int):
    if arity < 0:
        raise TypeError(f"Arity cannot be negative but received {arity}")
    try:
        actual_arity = positional_arity(func)
        has_positional_varargs = has_varargs(func)
    except TypeError:
        # This happens if [func] is a built in function or other function which signature is unknown.
        # If we cannot access [func]'s signature we cannot checks the correctness of arity => we silently fail
        return

    if (not has_positional_varargs and arity != actual_arity) or arity < actual_arity:
        raise TypeError(
            f"Received function {func} with {actual_arity} positional arguments but arity was less: {arity}"
        )


def __curry_internal(func: Callable[..., R], arity: int, passed_args: list = None) -> Callable:
    """
    For internal use by curry_explicit only!
    """
    if passed_args is None:
        passed_args = []

    __check_curry_arity(func, arity)

    if arity == 0:
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
