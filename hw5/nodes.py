from dataclasses import dataclass
from typing import Tuple, cast, Iterator, TypeVar, Generic

from hw5.comparable import Comparable

K = TypeVar("K", bound=Comparable)
V = TypeVar("V", bound=Comparable)

Entry = Tuple[K, V]


class Node(Generic[K, V]):
    """
    The base class for all treap nodes. Should have only 2 subclasses: EmptyNode, NotEmptyNode.
    K -- the type of keys in the treap
    V -- the type of priorities in the treap
    """

    def split(self, key: K) -> Tuple["Node[K, V]", "Node[K, V]"]:
        """
        The splitting operation as defined at https://en.wikipedia.org/wiki/Treap
        :param key: The key by which the split should be performed
        :return: Two subtrees: tht first contains all keys smaller than [key], the second contains all the other keys
        """
        ...

    def merge(self, other: "Node[K, V]") -> "Node[K, V]":
        """
        The merge operation as defined at https://en.wikipedia.org/wiki/Treap
        :param other: The other subtree which the current one should be merged with
        :return:
        """
        ...

    def __len__(self):
        """
        The number of nodes in the subtree
        """
        ...

    def ascending_order(self) -> Iterator[Entry]:
        """
        Iterator in the ascending order of keys
        """
        ...

    def descending_order(self) -> Iterator[Entry]:
        """
        Iterator in the descending order of keys
        """
        ...

    def __iter__(self):
        return self.ascending_order()

    def __contains__(self, key: K) -> bool:
        """
        Checks whether the subtree contains a node with key [key]
        """
        ...

    def __getitem__(self, key: K) -> V:
        """
        Returns a priority of the node with key [key].
        :raises KeyError if key is not found in the tree
        """
        ...

    def without_smallest_key(self) -> "Node[K, V]":
        """
        Returns the subtree without the node which key is the smallest
        """
        ...

    def remove_key(self, key: K) -> "Node[K, V]":
        """
        Returns the subtree without the node with key [key]
        :param key: The key to remove
        :return: The subtree without the [key]
        """
        if key not in self:
            raise KeyError(f"The key {key} is not present in the treap")
        (smaller_keys, not_smaller_keys) = self.split(key)
        assert isinstance(not_smaller_keys, NotEmptyNode)
        not_smaller_keys = cast(NotEmptyNode, not_smaller_keys)
        return smaller_keys.merge(not_smaller_keys.without_smallest_key())

    def insert_key(self, key: K, priority: V) -> "Node[K, V]":
        """
        Adds (immutably) the [key] with the specified [priority] to the tree
        :return: the new subtree
        """
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
    """
    The empty subtree that does not have children and a (key, priority) pair.
    """

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
    """
    The implementation of the non-empty treap subtree.
    """

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
        return NotEmptyNode(other.key, other.priority, self.merge(other.left), other.right)

    def without_smallest_key(self) -> "Node[K, V]":
        if not isinstance(self.left, NotEmptyNode):
            return self.right
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
        return key in self.left

    def __getitem__(self, key: K):
        if self.key == key:
            return self.priority
        elif self.key < key:
            return self.right[key]
        return self.left[key]
