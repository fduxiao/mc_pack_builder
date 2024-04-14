"""
This module provides classes making a command.

Basically, a command is just a string, but sometimes parts of that string is `computed`.
For example, an item may be used in a `give` method as `give @s item_id{CustomData:...}`,
while if you want to make chest with this item, you should then use
`{item:{id:item_id, tags:{CustomData}}}`. For the same :py:class:`mc_pack_builder.resources.Item`,
you may want to use item.resource_location(), item.as_str(), item.item_nbt for different purposes.
Thus, a part of a command is a callable returning a string, i.e., a class with __str__ method
"""
from functools import wraps
from nbtlib.tag import Base
from .natural_model import serialize_tag, py2nbt


class Command:
    """
    A command just collects a lot of parts, which can be mapped to string
    """
    def __init__(self, *parts, sep=' '):
        self.parts = parts
        self.joint = sep

    def force_str(self):
        self.parts = map(str, self.parts)
        return self

    def __call__(self, *args):
        return Command(*self.parts, *args)

    def __str__(self):
        return self.joint.join(map(str, self.parts))


def brace(*args, sep=', '):
    return Command('{', Command(*args, sep=sep), '}', sep='')


class Macro:
    def __init__(self, content):
        self.content = content

    def __str__(self):
        return f'${self.content}'


class Target:
    """
    The target selector
    """
    def __init__(self, var):
        self.var = var
        self.arguments = dict()
        self._scores = dict()
        self._nbt = dict()

    def __call__(self, **kwargs):
        self.arguments.update(kwargs)
        return self

    def scores(self, **kwargs):
        self._scores.update(kwargs)
        return self

    def __str__(self):
        # shallow copy
        arguments = self.arguments.copy()
        if self._scores:
            arguments['scores'] = self._scores
        if self._nbt:
            nbt = py2nbt(self._nbt)
            arguments['nbt'] = serialize_tag(nbt)
        if arguments:
            def parse_item(item):
                key, value = item
                if isinstance(value, Base):
                    value = serialize_tag(value)
                return f'{key}={value}'
            arg_str = ",".join(map(parse_item, arguments.items()))
            arg_str = f'[{arg_str}]'
        else:
            arg_str = ""
        return f'@{self.var}{arg_str}'

    def pos(self, x=None, y=None, z=None):
        if x is not None:
            self(x=x)
        if y is not None:
            self(y=y)
        if z is not None:
            self(z=z)
        return self

    def dist(self, distance):
        self(distance=distance)
        return self

    def sort(self, s):
        self(sort=s)
        return self

    def limit(self, n):
        self(limit=n)
        return self

    def type(self, target_type):
        self(type=target_type)
        return self

    def nbt(self, **kwargs):
        self._nbt.update(kwargs)
        return self

    @staticmethod
    def parse_item(item, with_count=True, custom_id=True, **kwargs):
        # to avoid a loop import
        from .resources import Item
        if isinstance(item, Item):
            if custom_id:
                custom_id = item.get('CustomID', None)
                if custom_id is not None:
                    item = item.custom_id()
            item = item.item_nbt(with_count, **kwargs)
        return item

    def selected_item(self, item, with_count=True, custom_id=True, **kwargs):
        self.nbt(SelectedItem=self.parse_item(item, with_count, custom_id, **kwargs))
        return self

    def item(self, item, with_count=True, custom_id=True, **kwargs):
        self.nbt(Item=self.parse_item(item, with_count, custom_id, **kwargs))
        return self


def at(var):
    return Target(var)


def at_s(**kwargs):
    return at('s')(**kwargs)


def at_e(**kwargs):
    return at('e')(**kwargs)


give = Command('give')
say = Command('say')
tell = Command('tell')
tellraw = Command('tellraw')
trigger = Command('trigger')
summon = Command('summon')
clear = Command('clear')
data = Command('data')


class ScoreBoard:
    """
    Represent the scoreboard command with an OOP style
    """
    def __init__(self, objective, criteria="dummy", display_name=None):
        self.objective = objective
        self.criteria = criteria
        self.display_name = display_name
        self.cmd = Command('scoreboard')
        self.cmd_obj = self.cmd('objectives')
        self.cmd_player = self.cmd('players')

    def add_objective(self):
        cmd = self.cmd_obj('add', self.objective, self.criteria)
        if self.display_name:
            cmd = cmd(self.display_name)
        return cmd

    # player functions
    def enable(self, target):
        return self.cmd_player('enable', target, self.objective)

    def set_player(self, target, score):
        return self.cmd_player('set', target, self.objective, score)

    def add_player(self, target, value=0):
        return self.cmd_player('add', target, self.objective, value)

    def get_player(self, target):
        return self.cmd_player('get', target, self.objective)

    def trigger(self, add_value=None, set_value=None):
        cmd = trigger(self.objective)
        if add_value:
            cmd = cmd('add', add_value)
        if set_value:
            cmd = cmd('set', set_value)
        return cmd

    def __lt__(self, other):
        return Command(self.objective, '=', '..', other - 1, sep='')

    def level_guard_cmds(self, min_score):
        yield execute().if_entity(at_s(type='player')).force_str().run(self.add_player(at_s(), 0))
        yield execute().if_entity(
            at_s(type='player', scores=brace(self < min_score))
        ).run('return fail')

    def level_guard(self, min_score):
        """used as a decorator"""
        def wrapper(func):
            @wraps(func)
            def wrapped():
                yield from self.level_guard_cmds(min_score)
                yield from func()
            return wrapped
        return wrapper


def scoreboard(objective):
    return ScoreBoard(objective)


class Execute:
    def __init__(self):
        self.modifications = list()
        self.condition_type = None
        self.condition_expr = None
        self.cmd_run = None

    def force_str(self):
        self.modifications = {k: str(v) for k, v in self.modifications}
        self.condition_type = str(self.condition_type)
        self.condition_expr = str(self.condition_expr)
        self.cmd_run = str(self.cmd_run)
        return self

    def modify(self, **kwargs):
        for k, v in kwargs.items():
            self.modifications.append((k, v))
        return self

    def as_(self, target):
        self.modifications.append(('as', target))
        return self

    def at(self, target):
        return self.modify(at=target)

    def align(self, align='xyz'):
        return self.modify(align=align)

    def condition(self, condition_type, condition):
        self.condition_type = condition_type
        self.condition_expr = condition
        return self

    def if_entity(self, condition):
        self.condition('if entity', condition)
        return self

    def run(self, cmd):
        self.cmd_run = cmd
        return self

    def __str__(self):
        modifications = " ".join(f'{k} {v}' for k, v in self.modifications)
        cmd = 'execute'
        if modifications != "":
            cmd += " " + modifications
        if self.condition_type:
            cmd += f" {self.condition_type} {self.condition_expr}"
        if self.cmd_run:
            cmd += f" run {self.cmd_run}"
        return cmd


execute = Execute
