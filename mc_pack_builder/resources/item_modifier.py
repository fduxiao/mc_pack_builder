"""
Item modifier.
"""
from .resource import Resource


class ItemModifier(Resource):
    """
    Item Modifier
    """
    def function(self, function):
        self.set_data('function', function)
        return self

    def count(self, count=1):
        self.set_data('count', count)
        return self

    def add(self, add=True):
        self.set_data('add', add)
        return self

    def __str__(self):
        return self.resource_location()
