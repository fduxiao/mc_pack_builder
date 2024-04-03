from enum import Enum
from ..pack import Dir
from ..resources import Tag


class TagType(Enum):
    blocks = "blocks"
    entity_types = "entity_types"
    fluids = "fluids"
    functions = "functions"
    game_events = "game_events"
    items = "items"


class Tags(Dir):
    """
    The tags direction
    """
    def __init__(self, namespace: str):
        super().__init__()
        self.namespace = namespace

    def tag(self, tag_type: str | TagType, name):
        if isinstance(tag_type, TagType):
            tag_type = tag_type.value
        tag = Tag(name, self.namespace)
        self.ensure_node(tag_type, Dir).add_json(f'{name}.json', tag)
        return tag

    def blocks(self, name):
        """add block tags"""
        return self.tag(TagType.blocks, name)

    def entity_types(self, name):
        """add entity type tags"""
        return self.tag(TagType.entity_types, name)

    def fluids(self, name):
        """add fluid tags"""
        return self.tag(TagType.fluids, name)

    def functions(self, name):
        """add function tags"""
        return self.tag(TagType.functions, name)

    def game_events(self, name):
        """add game event tags"""
        return self.tag(TagType.game_events, name)

    def items(self, name):
        """add item tags"""
        return self.tag(TagType.items, name)
