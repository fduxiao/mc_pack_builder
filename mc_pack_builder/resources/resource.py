"""
In minecraft, any resources like blocks/items/entities are described through a namespace:id.
Besides, if we want to `select` a resource, we sometimes want to also specify the nbt data,
e.g., minecraft:stone{CustomData: 123}. This module intends to provide a selector builder.
"""
from mc_pack_builder.natural_model import DictModel, NaturalModel


class Resource(DictModel):
    """
    This class represents a minecraft resource
    """

    def __init__(self, resource_id="", namespace="microsoft"):
        super().__init__()
        self.resource_id = resource_id
        self.namespace = namespace

    def resource_location(self):
        return f"{self.namespace}:{self.resource_id}"

    def as_str(self):
        return self.resource_location() + self.to_nbt()

    def __str__(self):
        return self.as_str()

    def set_data(self, key, value):
        self.dict[key] = value
        return self
