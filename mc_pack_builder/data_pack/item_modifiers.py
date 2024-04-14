from .namespaced import Namespaced


class ItemModifiers(Namespaced):
    """
    The tags direction
    """

    def new(self, path):
        modifier = self.item_modifier(path)
        self.add_json(f'{path}.json', modifier)
        return modifier
