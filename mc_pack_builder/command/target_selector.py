from ..natural_model import py2nbt, serialize_tag
from nbtlib import Base


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
        from ..resources import Item
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
