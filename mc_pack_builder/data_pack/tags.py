from enum import Enum
from .namespaced import Namespaced


class TagType(Enum):
    blocks = "blocks"
    entity_types = "entity_types"
    fluids = "fluids"
    functions = "functions"
    game_events = "game_events"
    items = "items"


class Tags(Namespaced):
    """
    The tags directory
    """

    def new(self, tag_type: str | TagType, name):
        if isinstance(tag_type, TagType):
            tag_type = tag_type.value
        tag = self.tag(name)
        self.dir(tag_type).add_json(f'{name}.json', tag)
        return tag

    def blocks(self, name):
        """add block tags"""
        return self.new(TagType.blocks, name)

    def entity_types(self, name):
        """add entity type tags"""
        return self.new(TagType.entity_types, name)

    def fluids(self, name):
        """add fluid tags"""
        return self.new(TagType.fluids, name)

    def functions(self, name):
        """add function tags"""
        return self.new(TagType.functions, name)

    def game_events(self, name):
        """add game event tags"""
        return self.new(TagType.game_events, name)

    def items(self, name):
        """add item tags"""
        return self.new(TagType.items, name)
