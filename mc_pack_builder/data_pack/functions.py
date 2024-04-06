from functools import update_wrapper
from pathlib import Path
from typing import IO

from ..pack import Dir, Leaf
from ..resources import Function


class FunctionLeaf(Leaf):
    def __init__(self, func: Function):
        self.func: Function = func

    def dump_to(self, file: IO):
        for i in self.func.gen_lines():
            file.write(f'{i}\n')


class Functions(Dir):
    def __init__(self, namespace="", prefix: Path | str = ""):
        super().__init__()
        self.namespace = namespace
        self.prefix = Path(prefix)

    def dir(self, path: str | Path) -> "Functions":
        return self.ensure_node(path, lambda: Functions(self.namespace, self.prefix / path))

    def new(self, path: str | Path):
        func = Function(resource_id=f'{self.prefix / path}', namespace=self.namespace)
        self.ensure_node(f'{path}.mcfunction', lambda: FunctionLeaf(func))
        return func

    def make(self, force_str=True):
        """
        used when make a function from generator
        @functions.define()
        def something():
            yield say("say1")
            yield say("say2")

        :param force_str: force to apply str to each line
        :return:
        """
        def decorator(func):
            result = self.new(func.__name__)
            body = func()
            if force_str:
                body = map(str, body)
            result.body(body)
            update_wrapper(result, func)
            return result

        return decorator
