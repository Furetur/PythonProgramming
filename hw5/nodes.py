from dataclasses import dataclass
from typing import Tuple, cast, Iterator, TypeVar, Generic

from hw5.comparable import Comparable

K = TypeVar("K", bound=Comparable)
V = TypeVar("V", bound=Comparable)

Entry = Tuple[K, V]


class Node(Generic[K, V]):
    def split(self, key: K) -> Tuple["Node[K, V]", "Node[K, V]"]:
        ...

    def merge(self, other: "Node[K, V]") -> "Node[K, V]":
        ...

    def __len__(self):
        ...

    def ascending_order(self) -> Iterator[Entry]:
        ...

    def descending_order(self) -> Iterator[Entry]:
        ...

    def __iter__(self):
        return self.ascending_order()

    def __contains__(self, key: K) -> bool:
        ...

    def __getitem__(self, key: K) -> V:
        ...

    def without_smallest_key(self) -> "Node[K, V]":
        ...

    def remove_key(self, key: K) -> "Node[K, V]":
        if key not in self:
            raise KeyError(key)
        (smaller_keys, not_smaller_keys) = self.split(key)
        assert isinstance(not_smaller_keys, NotEmptyNode)
        not_smaller_keys = cast(NotEmptyNode, not_smaller_keys)
        return smaller_keys.merge(not_smaller_keys.without_smallest_key())

    def insert_key(self, key: K, priority: V) -> "Node[K, V]":
        (smaller_keys, not_smaller_keys) = self.split(key)
        greater_keys = (
            not_smaller_keys
            if key not in not_smaller_keys
            else cast(NotEmptyNode, not_smaller_keys).without_smallest_key()
        )
        new_key_node = NotEmptyNode(key, priority, EmptyNode(), EmptyNode())
        return smaller_keys.merge(new_key_node).merge(greater_keys)


@dataclass(frozen=True)
class EmptyNode(Node[K, V]):
    def split(self, key: K) -> Tuple["EmptyNode[K, V]", "EmptyNode[K, V]"]:
        return EmptyNode(), EmptyNode()

    def merge(self, other: "Node[K, V]") -> "Node[K, V]":
        return other

    def __len__(self):
        return 0

    def ascending_order(self) -> Iterator[Entry]:
        yield from ()

    def descending_order(self) -> Iterator[Entry]:
        yield from ()

    def __contains__(self, key):
        return False

    def __getitem__(self, key):
        raise KeyError(key)


@dataclass(frozen=True)
class NotEmptyNode(Node[K, V]):
    key: K
    priority: V
    left: Node[K, V] = EmptyNode()
    right: Node[K, V] = EmptyNode()

    def split(self, key: K) -> Tuple["Node[K, V]", "Node[K, V]"]:
        if key > self.key:
            (smaller_keys, not_smaller_keys) = self.right.split(key)
            return NotEmptyNode(self.key, self.priority, self.left, smaller_keys), not_smaller_keys
        else:
            (smaller_keys, not_smaller_keys) = self.left.split(key)
            return smaller_keys, NotEmptyNode(self.key, self.priority, not_smaller_keys, self.right)

    def merge(self, other: "Node[K, V]") -> "Node[K, V]":
        if not isinstance(other, NotEmptyNode):
            return self
        other = cast(NotEmptyNode, other)
        if self.max_key() >= other.min_key():
            raise ValueError("Each key of the first tree should be smaller than any key in the second tree")
        if self.priority > other.priority:
            return NotEmptyNode(self.key, self.priority, self.left, self.right.merge(other))
        else:
            return NotEmptyNode(other.key, other.priority, self.merge(other.left), other.right)

    def without_smallest_key(self) -> "Node[K, V]":
        if not isinstance(self.left, NotEmptyNode):
            return self.right
        else:
            left = cast(NotEmptyNode, self.left)
            return NotEmptyNode(self.key, self.priority, left.without_smallest_key(), self.right)

    def __len__(self):
        return 1 + len(self.left) + len(self.right)

    def ascending_order(self) -> Iterator[Entry]:
        yield from self.left.ascending_order()
        yield self.key, self.priority
        yield from self.right.ascending_order()

    def descending_order(self) -> Iterator[Entry]:
        yield from self.right.descending_order()
        yield self.key, self.priority
        yield from self.left.descending_order()

    def min_key(self):
        key, _ = next(self.ascending_order())
        return key

    def max_key(self):
        key, _ = next(self.descending_order())
        return key

    def __contains__(self, key: K):
        if self.key == key:
            return True
        elif self.key < key:
            return key in self.right
        else:
            return key in self.left

    def __getitem__(self, key: K):
        if self.key == key:
            return self.priority
        elif self.key < key:
            return self.right[key]
        else:
            return self.left[key]
