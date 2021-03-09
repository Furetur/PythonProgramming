from copy import deepcopy
from typing import TypeVar, Callable, Union, cast, Protocol, runtime_checkable

from hw2.smart_args.no_value import NoValueType, NoValue

R = TypeVar("R", covariant=True)


@runtime_checkable
class MagicArgument(Protocol[R]):
    def __call__(self, actual_arg_value: Union[R, NoValueType]) -> R:
        ...


class Evaluated(MagicArgument[R]):
    """
    Magic argument default value which evaluates a function and returns its value as an argument value
    each time the actual argument is not passed to the function.
    """

    def __init__(self, get_default_value: Callable[[], R]):
        """
        :param get_default_value: function which returns the value of the argument
        when no value is passed to the function
        """
        if get_default_value is Isolated or isinstance(get_default_value, Isolated):
            raise TypeError("Evaluated cannot accept Isolated type or Isolated magic argument")
        self.get_default_value = get_default_value

    def __call__(self, actual_arg_value: Union[R, NoValueType]) -> R:
        """
        If no value is passed ([actual_arg_value] is NoValue) evaluates the [get_default_value] function
        and returns its result, otherwise returns the passed value
        :param actual_arg_value: the argument value that was passed to the smart function
        :return: actual argument value of the magic function
        """
        if actual_arg_value is NoValue:
            return self.get_default_value()
        else:
            return cast(R, actual_arg_value)


class Isolated(MagicArgument[R]):
    """
    Magic argument which deep copies the actual value that is passed to the magic function as a certain argument.
    Raises an error if nothing was passed to the magic function.
    """

    def __call__(self, actual_arg_value: Union[R, NoValueType]) -> R:
        """
        Deep copies [actual_arg_value] or raises an error if it is NoValue
        :param actual_arg_value: the actual value that was passed to the magic function
        :return: deep copied [actual_arg_value]
        """
        if actual_arg_value is NoValue:
            raise TypeError("One of Isolated keyword arguments did not receive a value")
        else:
            return deepcopy(cast(R, actual_arg_value))
