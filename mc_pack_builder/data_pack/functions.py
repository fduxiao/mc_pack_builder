from pathlib import Path
from typing import IO

from ..pack import Dir, Leaf
from ..resources import Function
from typing import Callable


class FunctionLeaf(Leaf):
    def __init__(self, func: Function):
        self.func: Function = func

    def dump_to(self, file: IO):
        for i in self.func.gen_lines():
            file.write(f'{i}\n')


class Functions(Dir):
    def __init__(self, namespace="", prefix: Path | str = "", data=None):
        super().__init__()
        self.namespace = namespace
        self.prefix = Path(prefix)

        if data is None:
            data = {}
        self.data = data

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        return self

    def on_load(self, *cmds):
        on_load = self.get('on_load')
        if on_load is not None:
            on_load(*cmds)
        return self

    def on_tick(self, *cmds):
        on_tick = self.get('on_tick')
        if on_tick is not None:
            on_tick(*cmds)

    def set_default(self, key, default):
        return self.data.setdefault(key, default)

    def dir(self, path: str | Path) -> "Functions":
        return self.ensure_node(path, lambda: Functions(self.namespace, self.prefix / path, self.data))

    def fork(self):
        functions = Functions(self.namespace, self.prefix, self.data)
        functions.nodes = self.nodes
        return self

    def new(self, path: str | Path = None, body=None) -> Function | Callable[[...], Function]:
        """
        Add a new function. This may be called as a decorator.
        If path is not None, then the :py:class:`Function` object is given.
        Otherwise, a decorator is returned using the function __name__ as path,
        and body will always be added as body

        :param path:
        :param body:
        :return:
        """

        def make_func():
            func = Function(
                resource_id=f'{self.prefix / path}',
                namespace=self.namespace,
            )

            if body is not None:
                func.body(body)

            return FunctionLeaf(func)

        if path is not None:
            leaf = self.ensure_node(f'{path}.mcfunction', make_func)
            return leaf.func
        else:
            def wrapper(yield_func):
                nonlocal path
                path = yield_func.__name__
                func = self.ensure_node(f'{yield_func.__name__}.mcfunction', make_func).func
                func.make(yield_func)
                return func
            return wrapper
