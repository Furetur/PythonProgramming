from functools import update_wrapper
from inspect import getfullargspec, FullArgSpec
from typing import TypeVar, Generic, Callable, List, Tuple

from hw2.smart_args.no_value import NoValue
from hw2.smart_args.supported_magic_args import MagicArgument


def find_magic_kwargs(arg_spec: FullArgSpec) -> List[Tuple[str, MagicArgument]]:
    """
    Finds magic keyword arguments and their magic argument default values in the FullArgSpec
    :param arg_spec: argument specification of the researched function
    :return: list of tuples (keyword argument name, its magic argument default value)
    """
    kwonly_args = arg_spec.kwonlyargs
    kwarg_defaults = arg_spec.kwonlydefaults or {}
    return [
        (kwarg_name, kwarg_defaults[kwarg_name])
        for kwarg_name in kwonly_args
        if kwarg_name in kwarg_defaults and isinstance(kwarg_defaults[kwarg_name], MagicArgument)
    ]


R = TypeVar("R")


class SmartArgs(Generic[R]):
    def __init__(self, func: Callable[..., R]):
        args_data = getfullargspec(func)
        self.func = func
        self.positional_defaults = args_data.defaults
        self.magic_kwargs = find_magic_kwargs(args_data)
        self.check_magic_args_misuse()
        update_wrapper(self, func)

    def check_magic_args_misuse(self) -> None:
        if self.positional_defaults is not None and any(
            isinstance(default_value, MagicArgument) for default_value in self.positional_defaults
        ):
            raise TypeError("Magic arguments can only be used as default values for keyword-only arguments")

    def __call__(self, *args, **kwargs) -> R:
        for kwarg_name, magic_default_value in self.magic_kwargs:
            kwargs[kwarg_name] = magic_default_value(kwargs[kwarg_name] if kwarg_name in kwargs else NoValue)
        return self.func(*args, **kwargs)


def smart_args(func: Callable[..., R]) -> Callable[..., R]:
    """
    SmartArgs decorator which turns a regular function into a magic function.
    Analyzes function default argument values and applies magic arguments where needed.
    *Magic args misuse*: magic args cannot be used as positional arguments. In other words you cannot
    use any magic value as a default value for a positional argument.
    :param func: a regular function
    """
    return SmartArgs(func)
