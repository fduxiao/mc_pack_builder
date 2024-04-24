
class Give:
    def __init__(self, target=None, item=None, count=None):
        self._target = target
        self._item = item
        self._count = count

    def to(self, target):
        self._target = target
        return self

    def item(self, item):
        self._item = item
        return self

    def __str__(self):
        from ..resources import Item
        item = self._item
        if isinstance(item, Item):
            item = item.as_str()
        cmd = f'give {self._target} {item}'
        if self._count is not None:
            cmd += f' {self._count}'
        return cmd


give = Give
