from functools import update_wrapper
from pathlib import Path
from typing import IO

from ..pack import Dir, Leaf
from ..resources import Function
from ..natural_model import Box


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

    def new(self, path: str | Path, before_body=None):
        func = Function(
            resource_id=f'{self.prefix / path}',
            namespace=self.namespace,
            before_body=before_body
        )
        self.ensure_node(f'{path}.mcfunction', lambda: FunctionLeaf(func))
        return func

    def make(self, before_body=None):
        """
        used when make a function from generator
        @functions.define()
        def something():
            yield say("say1")
            yield say("say2")

        :param before_body: whether to add extra guarding commands
        :return:
        """
        def decorator(func):
            result = self.new(func.__name__, before_body=before_body)
            body = func()
            result.body(body)
            update_wrapper(result, func)
            return result

        return decorator


class LevelGuard(Functions):
    """
    The function adder with guard
    """
    def __init__(self, namespace="", prefix: Path | str = "", objective=None):
        super().__init__(namespace, prefix)

        self.objective = objective

    def dir(self, path: str | Path) -> "LevelGuard":
        return self.ensure_node(path, lambda: LevelGuard(self.namespace, self.prefix / path, self.objective))

    def get_guard_cmd(self, min_score):
        return [
            Box(get_cast=lambda _: f'execute if entity @s[type=player] run '
                                   f'scoreboard players add @s {self.objective} 0'),
            Box(get_cast=lambda _: 'execute if entity @s[type=player, scores={%s}] run '
                                   'return fail' % f'{self.objective}=..{min_score-1}')
        ]

    def guarded_new(self, path: str | Path, min_score):
        func = self.new(path)
        func.before_body = self.get_guard_cmd(min_score)
        return self

    def guarded_make(self, min_score):
        return self.make(before_body=self.get_guard_cmd(min_score))
