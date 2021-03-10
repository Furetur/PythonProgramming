from functools import wraps
from typing import Callable


def uncurry_explicit(func: Callable, arity: int) -> Callable:
    """
    Uncurries a function.
    :param func: any function of type (a_1) -> (a_2) -> ... -> (a_n) -> R or () -> R
    :param arity: should be n if curried function is of type (a_1) -> (a_2) -> ... -> (a_n) -> R
    should be 0 if () -> R
    :return: uncurried function of type (a_1, ..., a_n) -> R or () -> R
    """

    @wraps(func)
    def uncurried_function(*args):
        if len(args) != arity:
            raise TypeError(f"Arity is {arity} but provided {len(args)} arguments")
        if arity == 0:
            return func()
        curried_result = func
        for arg in args:
            curried_result = curried_result(arg)
        return curried_result

    return uncurried_function
