"""
Tags available for item. Sometimes we want to add a chest with certain items. This time,
we have to use {item:{id:...}}, so I provided a different item_nbt method in this module.
"""
import json

from ..natural_model import Field, nbt, DictModel, py2nbt, serialize_tag
from .enchantments import Enchantment
from .resource import Resource


def parse_color(x):
    """
    In display tag, a color is an int. I shall allow other formats
    like an RGB tuple or #RRGGBB
    """
    if isinstance(x, int):
        return x
    if isinstance(x, tuple):
        r, g, b = x
        return (r << 16) | (g << 8) | b
    if isinstance(x, str):
        colors = {
            "black": 0x000000, "white": 0xFFFFFF,
            "red": 0xFF0000, "green": 0x00FF00, "blue": 0x0000FF
        }
        color = colors.get(x)
        if color is not None:
            return color
        x = x.split('#')[-1]
        x = int(x, 16)
        return x
    raise ValueError(f"Unknown color {x}")


class Display(DictModel):
    display_name = Field("Name", cast=str)
    lore: list = Field("Lore", default=[])
    color = Field(cast=parse_color)


class CustomID(dict):
    def __str__(self):
        return serialize_tag(py2nbt(self))


class Item(Resource):
    _count: int = None

    @property
    def count(self):
        """
        count for putting side a tag

        :return:
        """
        return self._count

    @count.setter
    def count(self, value):
        self._count = value

    def item_nbt(self, with_count=True, **kwargs):
        """
        used when putting in a tag

        :return:
        """
        data = {
            "id": nbt.String(self.resource_location()),
            "tag": self.dump_nbt(),
            **kwargs
        }
        if with_count and self.count is not None:
            data['count'] = nbt.Int(self.count)
        return nbt.Compound(data)

    def custom_id(self, custom_id=None, count: bool | int = False):
        """
        used when one to distinguish items through a unique id
        """
        if custom_id is not None:
            self.set_data('CustomID', custom_id)
            return self
        custom_id = self.get('CustomID', None)
        if custom_id is None:
            raise KeyError('Custom ID is not set')
        result = Item(self.resource_id, self.namespace)
        result.custom_id(custom_id)
        return result

    enchantments: list = Field("Enchantments", default=[])

    def enchant(self, *enchantments: Enchantment):
        self.enchantments.extend(enchantments)
        return self

    stored_enchantments: list = Field("StoredEnchantments", default=[])

    def store_enchantment(self, enchantment: Enchantment):
        self.stored_enchantments.append(enchantment.dump())
        return enchantment

    def entity_tag(self, tag):
        self.set_data("EntityTag", tag)

    _display = Display(name="display")

    def display_name(self, name):
        if not isinstance(name, str):
            name = str(name)
        if not name.startswith('{'):
            name = json.dumps({"text": name})
        self._display.display_name = name
        return self

    def display_color(self, color):
        self._display.color = color
        return self

    def lore(self, *args):
        lores = []
        for one in args:
            if not isinstance(one, str):
                one = str(one)
            if not one.startswith('{'):
                one = json.dumps({"text": one})
            lores.append(one)
        self._display.lore.extend(lores)
        return self

    def unbreakable(self, unbreakable=True):
        self.set_data("Unbreakable", unbreakable)
        return self

    def title(self, title):
        self.set_data("title", title)
        return self

    def author(self, author):
        self.set_data("author", author)
        return self

    _pages: list = Field('pages', default=[], cast=list)

    def clear_pages(self):
        self._pages.clear()
        return self

    def pages(self, *pages):
        self._pages.extend(pages)
        return self
