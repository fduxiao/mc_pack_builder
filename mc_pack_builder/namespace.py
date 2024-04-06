"""
In minecraft, both resource packs and data packs are based on a namespace, which is then used
to locate resources. This module contains such a class modeling a namespace. And of course, a
resource is some id inside a namespace.
"""

from .resources import enchantment, Resource, Item, Tag, Function


class Namespace:
    """
    The namespace class
    """

    def __init__(self, name):
        self.name = name

    def __call__(self, resource_id):
        return f'{self.name}:{resource_id}'

    def enchantment(self, enchantment_id, lvl=1):
        return enchantment(self(enchantment_id), lvl)

    def resource(self, resource_id):
        return Resource(resource_id, self.name)

    def item(self, item_id):
        return Item(item_id, self.name)

    def tag(self, tag_id):
        return Tag(tag_id, self.name)

    def function(self, function_id, body=None):
        return Function(body, function_id, self.name)
