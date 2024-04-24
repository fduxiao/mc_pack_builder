"""
This module provides classes making a command.

Basically, a command is just a string, but sometimes parts of that string is `computed`.
For example, an item may be used in a `give` method as `give @s item_id{CustomData:...}`,
while if you want to make chest with this item, you should then use
`{item:{id:item_id, tags:{CustomData}}}`. For the same :py:class:`mc_pack_builder.resources.Item`,
you may want to use item.resource_location(), item.as_str(), item.item_nbt for different purposes.
Thus, a part of a command is a callable returning a string, i.e., a class with __str__ method
"""


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


say = Command('say')
tell = Command('tell')
tellraw = Command('tellraw')
trigger = Command('trigger')
summon = Command('summon')
clear = Command('clear')
data = Command('data')
