from ..pack import Pack, Dir
from ..natural_model import DictModel, Field
from ..namespace import Namespace
from .tags import Tags
from .recipes import Recipes


class MCMeta(DictModel):
    desc = Field("pack/description")
    format = Field("pack/pack_format")


class DatapackNamespace(Dir):
    """
    The namespace of a datapack is a branch in the :py:class:`mc_pack_builder.pack.FSTree`
    To add some data to the datapack, you need to add files to the namespace directory.
    This class serves for that purpose
    """
    def __init__(self, name=None):
        super().__init__()
        self.namespace = Namespace(name)

    @property
    def tags(self):
        return self.ensure_node("tags", lambda: Tags(self.namespace.name))

    @property
    def recipes(self):
        return self.ensure_node("recipes", Recipes)


class DataPack(Pack):
    def __init__(self, desc: str, pack_format: int):
        super().__init__()
        self.mcmeta: MCMeta = self.add_json("pack.mcmeta", MCMeta())
        self.mcmeta.desc = desc
        self.mcmeta.format = pack_format
        self.data = self.dir("data")

    def namespace(self, name):
        return self.data.ensure_node(name, lambda: DatapackNamespace(name))
