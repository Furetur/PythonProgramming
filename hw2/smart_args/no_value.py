from typing import Type


class NoValue:
    """
    *This should be used as a singleton object!*. For example: `a = NoValue`.
    NoValue object is passed to the magic argument when no value is passed to the magic function as that specific arg.
    In other words, when magic argument does not receive any value (it receives [NoValue]).
    """

    def __init__(self):
        raise TypeError("Type NoValue cannot be initialized. Treat it as a singleton object.")


NoValueType = Type[NoValue]
