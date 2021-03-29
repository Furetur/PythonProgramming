import inspect
from functools import update_wrapper
from typing import TypeVar, Generic, Callable, Tuple, Dict, Any

R = TypeVar("R")


class WithRuntimeCheckedParamTypes(Generic[R]):
    def __init__(self, function: Callable[..., R], arg_types: Tuple[type, ...], kwarg_types: Dict[str, type]):
        try:
            argspec = inspect.getfullargspec(function)
            self.arg_names = argspec.args
            self.kwonly_names = argspec.kwonlyargs
        except TypeError:
            raise TypeError("Cannot check runtime types of this function, because Python does not allow it.")
        self.function = function
        self.arg_types = arg_types
        self.kwarg_types = kwarg_types
        update_wrapper(self, function)

    def check_positional_arg_type(self, arg_position: int, arg_value: Any):
        if arg_position < len(self.arg_types):
            expected_type: type = self.arg_types[arg_position]
            if not isinstance(arg_value, expected_type):
                raise TypeError(
                    f"Expected positional argument #{arg_position} of type {expected_type} but received: {type(arg_value)}"
                )

    def check_named_arg_type(self, arg_name: str, arg_value: Any):
        if arg_name in self.arg_names:
            position = self.arg_names.index(arg_name)
            self.check_positional_arg_type(position, arg_value)
        elif arg_name in self.kwonly_names and arg_name in self.kwarg_types:
            expected_type: type = self.kwarg_types[arg_name]
            if not isinstance(arg_value, expected_type):
                raise TypeError(
                    f"Expected positional argument `{arg_name}` of type {expected_type} but received: {type(arg_value)}"
                )

    def check_arg_types(self, args, kwargs):
        for arg_position, arg_value in enumerate(args):
            self.check_positional_arg_type(arg_position, arg_value)
        for arg_name, arg_value in kwargs.items():
            self.check_named_arg_type(arg_name, arg_value)

    def __call__(self, *args, **kwargs) -> R:
        self.check_arg_types(args, kwargs)
        return self.function(*args, **kwargs)


def takes(*args: type, **kwargs: type):
    def decorator(function: Callable[..., R]) -> Callable[..., R]:
        return WithRuntimeCheckedParamTypes(function, args, kwargs)

    return decorator


takes(int)(print)
