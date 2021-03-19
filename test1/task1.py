from dataclasses import dataclass
from datetime import datetime
from functools import update_wrapper
from typing import TypeVar, Generic, Callable, Iterable, List


@dataclass
class FunctionCallInfo:
    invocation_time: datetime
    args: tuple
    kwargs: dict


R = TypeVar("R")


class SpyFunction(Generic[R]):
    def __init__(self, function: Callable[..., R]):
        self.function = function
        self.call_info_history: List[FunctionCallInfo] = []
        update_wrapper(self, function)

    def get_call_info(self) -> Iterable[FunctionCallInfo]:
        for call_info in self.call_info_history:
            yield call_info

    def __call__(self, *args, **kwargs) -> R:
        function_call = FunctionCallInfo(datetime.now(), args, kwargs)
        self.call_info_history.append(function_call)
        return self.function(*args, **kwargs)


def spy(function: Callable[..., R]) -> SpyFunction[R]:
    return SpyFunction(function)


def get_usage_statistic(function: SpyFunction[R]) -> Iterable[FunctionCallInfo]:
    return function.get_call_info()
