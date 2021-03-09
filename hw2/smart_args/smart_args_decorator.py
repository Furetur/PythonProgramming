from inspect import getfullargspec
from typing import TypeVar, Generic, Callable

from hw2.smart_args.no_value import NoValue
from hw2.smart_args.supported_magic_args import MagicArgument


class MagicArgumentsMisuseError(TypeError):
    """
    The error that is raised when magic arguments are used where they should not be used.
    """

    pass


R = TypeVar("R")


class SmartArgs(Generic[R]):
    def __init__(self, func: Callable[..., R]):
        args_data = getfullargspec(func)
        self.func = func
        self.positional_defaults = args_data.defaults
        self.kwargs_defaults = args_data.kwonlydefaults or {}
        self.magic_kwarg_names = [name for name in args_data.kwonlyargs if self.has_magic_default_value(name)]
        self.check_magic_args_misuse()

    def check_magic_args_misuse(self) -> None:
        if self.positional_defaults is not None and any(
            isinstance(default_value, MagicArgument) for default_value in self.positional_defaults
        ):
            raise MagicArgumentsMisuseError(
                "Magic arguments can only be used as default values for keyword-only arguments"
            )

    def has_magic_default_value(self, kwarg_name: str) -> bool:
        return kwarg_name in self.kwargs_defaults and isinstance(self.kwargs_defaults[kwarg_name], MagicArgument)

    def __call__(self, *args, **kwargs) -> R:
        for kwarg_name in self.magic_kwarg_names:
            magic_default_argument = self.kwargs_defaults[kwarg_name]
            kwargs[kwarg_name] = magic_default_argument(kwargs[kwarg_name] if kwarg_name in kwargs else NoValue)
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
