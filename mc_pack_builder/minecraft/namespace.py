from mc_pack_builder.namespace import Namespace
from .enchantments import Enchantment
from . import items


class Minecraft(Namespace):
    def __init__(self):
        super().__init__("minecraft")

    enchantments = Enchantment()

    def written_book(self, title, author, pages=None):
        book = items.Book("written_book", self.name)
        book.title(title).author(author)
        if pages is not None:
            book.pages(*pages)
        return book
