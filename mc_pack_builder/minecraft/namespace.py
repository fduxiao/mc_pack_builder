from mc_pack_builder.namespace import Namespace, Item
from .enchantments import Enchantment
from .item_modifiers import ItemModifierFunctions
from . import items


class CustomStat(Namespace):
    def __call__(self, item):
        if isinstance(item, Item):
            item = item.statistics_name()
        return f'{self.name}:{item}'


class SelectorType:
    item = "minecraft:item"
    armor_stand = "minecraft:armor_stand"


class Minecraft(Namespace):
    used = CustomStat('minecraft.used')
    type = SelectorType

    def __init__(self):
        super().__init__("minecraft")

    enchantments = Enchantment()
    item_modifier_functions = ItemModifierFunctions()

    def written_book(self, title, author, pages=None):
        book = items.Book("written_book", self.name)
        book.title(title).author(author)
        if pages is not None:
            book.pages(*pages)
        return book

    def carrot_stick(self):
        return self.item("carrot_on_a_stick")

    def paper(self):
        return self.item('paper')

    def emerald(self):
        return self.item('emerald')
