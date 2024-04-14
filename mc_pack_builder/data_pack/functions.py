from functools import partial
from typing import IO, Callable

from .. import FileSystem
from ..pack import Leaf
from ..resources import Function


from . namespaced import Namespaced, Path


class FunctionLeaf(Leaf):
    def __init__(self, func: Function):
        self.func: Function = func

    def dump_to(self, file: IO):
        for i in self.func.gen_lines():
            file.write(f'{i}\n')


class Functions(Namespaced):
    def on_load(self, *cmds):
        on_load = self.get('on_load')
        if on_load is not None:
            on_load(*cmds)
        return self

    def on_tick(self, *cmds):
        on_tick = self.get('on_tick')
        if on_tick is not None:
            on_tick(*cmds)

    def post_new(self, func):
        return func

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
            func = self.function(path)

            if body is not None:
                func.body(body)

            return FunctionLeaf(func)

        if path is not None:
            leaf = self.ensure_node(f'{path}.mcfunction', make_func)
            return self.post_new(leaf.func)
        else:
            def wrapper(yield_func):
                nonlocal path
                path = yield_func.__name__
                func = self.ensure_node(f'{yield_func.__name__}.mcfunction', make_func).func
                func.make(yield_func)
                return self.post_new(func)
            return wrapper

    def scoreboard_positive(self, objective, criteria="dummy", tree_dir=None):
        if tree_dir is None:
            tree_dir = f"trigger_tree_{objective}"
        scoreboard_positive: ScoreboardPositive = self.fork(
            partial(ScoreboardPositive, objective=objective, tree_dir=tree_dir)
        )
        self.on_load(f'scoreboard objectives add {objective} {criteria}')
        return scoreboard_positive

    def trigger_group(self, objective, tree_dir=None):
        if tree_dir is None:
            tree_dir = f"trigger_tree_{objective}"

        trigger_group: TriggerGroup = self.fork(partial(TriggerGroup, objective=objective, tree_dir=tree_dir))
        self.on_load(f'scoreboard objectives add {objective} trigger')
        self.on_load(trigger_group.enable())
        return trigger_group


class ScoreboardPositive(Functions):
    """
    when a scoreboard objective is set positive
    """
    def __init__(self, namespace="", prefix: Path | str = "", data=None, nodes=None, *,
                 objective=None, tree_dir: str | Path = None):
        super().__init__(namespace, prefix, data, nodes)
        if objective:
            self.data['objective'] = objective
        if tree_dir:
            self.ensure_node(tree_dir, lambda: TreeBuilder(self.namespace, self.prefix / tree_dir, self.data))

    @property
    def run_positive(self) -> Function:
        return self.data.get('run_positive')

    def post_new(self, func):
        self.run_positive.extend(func())
        return func


class TriggerGroup(Functions):
    """
    You may want to have a non-privilege player use /function command, but usually, this
    command cannot be used by a player with level 0. The solution is to use a scoreboard
    objective with trigger. When one want to call a function, he/she just triggers the
    corresponding objective. A tick function will then test whether the objective is the
    desired value and call the function.

    The TriggerGroup is designed for that purpose. To use it, you have to add an objective
    in on_load, and make a tick function to test it. The problem is that if you have thousands
    of objectives to check, then it may take a lot of time. Thus, a search tree is also provided
    for the trigger_group. The tick function and the search tree are store in a directory called
    tree_dir as functions.
    """
    def __init__(self, namespace="", prefix: Path | str = "", data=None, nodes=None, *, objective=None, tree_dir=None):
        super().__init__(namespace, prefix, data, nodes)
        if objective:
            self.data['objective'] = objective
        if tree_dir:
            # After called, the trigger_group just forks a new :py:class:`TriggerGroup` class.
            # The existing node is not changed. Thus, we cannot just overload the `dump` method.
            # Instead, a new class describing the dump phenomenon is needed.
            self.ensure_node(tree_dir, lambda: TreeBuilder(self.namespace, self.prefix / tree_dir, self.data))

    @property
    def objective(self):
        return self.get('objective')

    @property
    def functions(self) -> dict:
        return self.set_default('functions', {})

    @property
    def max_trigger_value(self):
        return self.get('function_max', 0)

    @max_trigger_value.setter
    def max_trigger_value(self, x):
        self.set('function_max', x)

    def enable(self, target='@a'):
        return f'scoreboard players enable {target} {self.objective}'

    def get_trigger(self, trigger_value=None):
        if trigger_value in self.functions:
            raise KeyError(f"duplicated key {trigger_value}")
        if trigger_value is None:
            trigger_value = self.max_trigger_value + 1
        self.max_trigger_value = max(trigger_value, self.max_trigger_value)
        return self.objective, trigger_value

    def new(self, path: str | Path = None, body=None, trigger_value=None) -> Function | Callable[[...], Function]:
        result = super().new(path, body)
        objective, trigger_value = self.get_trigger(trigger_value)
        if isinstance(result, Function):
            result.trigger(objective, trigger_value)
            self.functions[trigger_value] = result
            return result

        # then result is the wrapper. Make a new one
        def wrapper(yield_func):
            func: Function = result(yield_func)
            func.trigger(objective, trigger_value)
            self.functions[trigger_value] = func
            return func
        return wrapper


class TreeBuilder(Functions):
    """
    Help build the trigger tree in the trigger_tree directory
    """
    def __init__(self, namespace="", prefix: Path | str = "", data=None):
        super().__init__(namespace, prefix, data)
        self.tree_func = self.new('tick')
        self.data['run_positive'] = self.new('run_positive')
        self.tree_func.extend(f'execute as @a at @s if entity @s[scores={self.make_scores("1..")}] '
                              f'run {self.run_positive()}')
        self.on_tick(f'execute as @a at @s run {self.tree_func()}')

    # we also need the following two as in TriggerGroup
    @property
    def objective(self):
        return self.get('objective')

    @property
    def functions(self) -> dict:
        return self.set_default('functions', {})

    # for extra run_positive functions
    @property
    def run_positive(self) -> functions:
        return self.get('run_positive')

    def make_scores(self, value):
        scores = f'{self.objective}=%s' % value
        scores = '{%s}' % scores
        return scores

    def dump(self, rel_path: Path, fs: FileSystem):
        # build the tick function
        for trigger_value, func in self.functions.items():
            self.tree_func.extend(f'execute if entity @s[scores={self.make_scores(trigger_value)}] run {func()}')
        self.tree_func.extend(
            f'execute if entity @s[scores={self.make_scores("0..")}] run scoreboard players set @s {self.objective} 0',
            f'execute if entity @s[scores={self.make_scores("0..")}] run scoreboard players enable @s {self.objective}',
        )
        # call the usual dump function
        return super().dump(rel_path, fs)
