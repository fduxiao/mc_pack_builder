"""
Tags available for item. Sometimes we want to add a chest with certain items. This time,
we have to use {item:{id:...}}, so I provided a different item_nbt method in this module.
"""

from ..natural_model import Field, nbt
from .enchantments import Enchantment
from .resource import Resource


class Item(Resource):
    _count: int = 1

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
            "tags": self.dump_nbt(),
            **kwargs
        }
        if with_count:
            data['count'] = nbt.Int(self.count)
        return nbt.Compound(data)

    enchantments: list = Field("Enchantments", default=[])

    def enchant(self, *enchantments: Enchantment):
        for enc in enchantments:
            self.enchantments.append(enc.dump())
        return self

    stored_enchantments: list = Field("StoredEnchantments", default=[])

    def store_enchantment(self, enchantment: Enchantment):
        self.stored_enchantments.append(enchantment.dump())
        return enchantment

    def unbreakable(self, unbreakable=True):
        self.set_data("Unbreakable", unbreakable)
        return self
