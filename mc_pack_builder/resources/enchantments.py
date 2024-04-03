"""
collect all enchantments
"""
from ..natural_model import DictModel, Field


class Enchantment(DictModel):
    """
    Enchantment class
    """
    _id = Field("id", cast=str)

    def id(self, new_id=None):
        if new_id is None:
            return self._id
        self._id = new_id
        return self

    _lvl = Field("lvl")

    def lvl(self, lvl=None):
        if lvl is None:
            return self.lvl
        self._lvl = lvl
        return self


def enchantment(enchantment_id, lvl=1):
    return Enchantment().id(enchantment_id).lvl(lvl)
