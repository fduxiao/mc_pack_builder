"""
In minecraft, any resources like blocks/items/entities are described through a namespace:id.
Besides, if we want to `select` a resource, we sometimes want to also specify the nbt data,
e.g., minecraft:stone{CustomData: 123}. This module intends to provide a selector builder.
"""
from ..natural_model import DictModel, NaturalModel


class Resource(DictModel):
    """
    This class represents a minecraft resource
    """

    def __init__(self, resource_id="", namespace="minecraft"):
        super().__init__()
        self.resource_id = resource_id
        self.namespace = namespace

    def resource_location(self):
        return f"{self.namespace}:{self.resource_id}"

    def statistics_name(self):
        """when used as a custom statistics"""
        return f"{self.namespace}.{self.resource_id}"

    def as_str(self):
        return self.resource_location() + self.to_nbt()

    def __str__(self):
        return self.as_str()

    def set_data(self, key, value):
        self.dict[key] = value
        return self


class ResourceList(Resource):
    def __init__(self, resource_id="", namespace="minecraft"):
        super().__init__()
        self.resource_id = resource_id
        self.namespace = namespace
        self.data: list[NaturalModel] = []

    def dump(self):
        return [one.dump() for one in self.data]

    def append(self, one):
        self.data.append(one)
