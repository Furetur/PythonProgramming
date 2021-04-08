from typing import Tuple, Iterator, MutableMapping, TypeVar

from hw5.comparable import Comparable
from hw5.nodes import Node, EmptyNode

K = TypeVar("K", bound=Comparable)
V = TypeVar("V", bound=Comparable)

Entry = Tuple[K, V]


class Treap(MutableMapping):
    """
    A treap data structure as defined at https://en.wikipedia.org/wiki/Treap
    """

    def __init__(self):
        """
        Creates an initially empty treap
        """
        self.node: Node[K, V] = EmptyNode()

    def __contains__(self, key: K):
        """
        Checks if the treap contains a node with the [key]
        """
        return key in self.node

    def __getitem__(self, key: K) -> V:
        """
        Returns the priority of the node with the [key]
        """
        return self.node[key]

    def __setitem__(self, key: K, value: V):
        """
        Sets a node priority or adds a new node with the given priority.
        :param key: The node's key
        :param value: The node's priority
        """
        self.node = self.node.insert_key(key, value)

    def __delitem__(self, key: K):
        """
        Removes a key from the treap
        """
        self.node = self.node.remove_key(key)

    def __len__(self):
        """
        The number of keys stored on the treap
        """
        return len(self.node)

    def ascending_order(self) -> Iterator[Entry]:
        """
        Returns the iterator over the treap which yields (key, priority) pairs in the keys ascending order.
        """
        return self.node.ascending_order()

    def descending_order(self) -> Iterator[Entry]:
        """
        Returns the iterator over the treap which yields (key, priority) pairs in the keys descending order.
        """
        return self.node.descending_order()

    def __iter__(self) -> Iterator[K]:
        """
        Returns the iterator over the treap which yields keys in the ascending order
        """
        return map(lambda x: x[0], self.node.__iter__())
