"""
For those FSTree nodes under some namespace, they share a common behavior of calculate the path.
This module intends to provide such a base class
"""
from ..pack import Dir, Path
from ..namespace import Namespace
from typing import Self, TypeVar, Callable


T = TypeVar('T')


class Namespaced(Dir):
    def __init__(self, namespace: str | Namespace = "", prefix: Path | str = "", data=None, nodes=None):
        super().__init__(nodes)
        self.namespace = Namespace(namespace)
        self.prefix = Path(prefix)

        if data is None:
            data = {}
        self.data = data

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        return self

    def set_default(self, key, default):
        return self.data.setdefault(key, default)

    def dir(self, path: str | Path) -> Self:
        node = self.ensure_node(path, lambda: type(self)(self.namespace.name, self.prefix / path, self.data))
        if not isinstance(node, type(self)):
            node = type(self)(self.namespace.name, self.prefix / path, self.data, node.nodes)
        return node

    def fork(self, fork_type: Callable[[...], T] = None, copy=True) -> T:
        if fork_type is None:
            fork_type = type(self)
        data = self.data
        if copy:
            data = data.copy()
        functions = fork_type(self.namespace.name, self.prefix, data, self.nodes)
        return functions

    # namespace related functions
    def get_id(self, path):
        return f'{self.prefix / path}'

    def tag(self, path):
        return self.namespace.tag(self.get_id(path))

    def function(self, path):
        return self.namespace.function(self.get_id(path))

    def item_modifier(self, path):
        return self.namespace.item_modifier(self.get_id(path))
