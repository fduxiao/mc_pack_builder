from mc_pack_builder import TextBase, Item, Text


class Book(Item):
    def pages(self, *pages):
        targets = []
        for page in pages:
            if isinstance(page, str):
                page = Text(page)
            if isinstance(page, TextBase):
                targets.append(page.json())
            else:
                targets.append(page)
        return super().pages(*targets)
