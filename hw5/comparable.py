from typing import Protocol, TypeVar, Any


class Comparable(Protocol):
    def __eq__(self, other: Any) -> bool:
        ...

    def __lt__(self, other: Any) -> bool:
        ...
