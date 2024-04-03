from ..natural_model import Field
from .resource import Resource


class Tag(Resource):
    """
    The tag used in a datapack
    """
    replace: bool = Field(default=False)
    values: list = Field(default=[])

    def tag_id(self):
        return f'#{super().resource_location()}'

    def add(self, *values):
        for v in values:
            if isinstance(v, Tag):
                self.values.append(v.tag_id())
            elif isinstance(v, Resource):
                self.values.append(v.resource_location())
            else:
                self.values.append(v)
        return self
