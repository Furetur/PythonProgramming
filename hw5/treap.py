from dataclasses import dataclass
from typing import Optional, Tuple, cast, Iterator, MutableMapping, TypeVar, Container

from hw5.comparable import Comparable
from hw5.nodes import Node, EmptyNode

K = TypeVar("K", bound=Comparable)
V = TypeVar("V", bound=Comparable)

Entry = Tuple[K, V]


class Treap(MutableMapping[K, V]):
    def __init__(self):
        self.node: Node[K, V] = EmptyNode()

    def __contains__(self, key: object):
        return key in self.node

    def __getitem__(self, key: K) -> V:
        return self.node[key]

    def __setitem__(self, key: K, value: V):
        self.node = self.node.insert_key(key, value)

    def __delitem__(self, key: K):
        self.node = self.node.remove_key(key)

    def __len__(self):
        return len(self.node)

    def pre_order(self) -> Iterator[Entry]:
        return self.node.ascending_order()

    def post_order(self) -> Iterator[Entry]:
        return self.node.descending_order()

    def __iter__(self) -> Iterator[K]:
        return map(lambda x: x[0], self.node.__iter__())
