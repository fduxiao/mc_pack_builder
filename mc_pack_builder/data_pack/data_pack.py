import weakref

from ..pack import Pack, Dir
from ..natural_model import DictModel, Field
from ..namespace import Namespace
from ..resources import Resource
from .tags import Tags
from .recipes import Recipes
from .functions import Functions


class DatapackNamespace(Dir):
    """
    The namespace of a datapack is a branch in the :py:class:`mc_pack_builder.pack.FSTree`
    To add some data to the datapack, you need to add files to the namespace directory.
    This class serves for that purpose
    """
    def __init__(self, name=None, datapack: "DataPack" = None):
        super().__init__()
        self.namespace = Namespace(name)
        self._datapack = weakref.ref(datapack)
        self._on_load = None
        self._on_tick = None

    @property
    def datapack(self) -> "DataPack | None":
        if self._datapack is None:
            return None
        return self._datapack()

    @property
    def tags(self):
        return self.ensure_node("tags", lambda: Tags(self.namespace.name))

    @property
    def recipes(self):
        return self.ensure_node("recipes", Recipes)

    @property
    def functions(self):
        return self.ensure_node("functions", lambda: Functions(self.namespace.name, data={
            "on_load": self.on_load,
            "on_tick": self.on_tick,
        }))

    def on_load(self, *cmds):
        if self._on_load is None:
            self._on_load = self.functions.new('on_load')
            if self.datapack is not None:
                self.datapack.on_load(self._on_load)
        self._on_load.extend(*cmds)
        return self

    def on_tick(self, *cmds):
        if self._on_tick is None:
            self._on_tick = self.functions.new('on_tick')
            if self.datapack is not None:
                self.datapack.on_tick(self._on_tick)
        self._on_tick.extend(*cmds)
        return self

    def scoreboard(self, name):
        # to avoid loop import
        from ..command import ScoreBoard
        sb = ScoreBoard(name)
        self.on_load(sb.add_objective())
        return sb


class MCMeta(DictModel):
    desc = Field("pack/description")
    format = Field("pack/pack_format")


class DataPack(Pack):
    def __init__(self, desc: str, pack_format: int):
        super().__init__()
        self.mcmeta: MCMeta = self.add_json("pack.mcmeta", MCMeta())
        self.mcmeta.desc = desc
        self.mcmeta.format = pack_format
        self.data = self.dir("data")

    def namespace(self, name):
        return self.data.ensure_node(name, lambda: DatapackNamespace(name, self))

    def add_func_tags(self, target, *args):
        """
        add functions that will be executed when then function is load
        """
        tags = self.namespace("minecraft").tags.functions(target)
        for one in args:
            if isinstance(one, Resource):
                one = one.resource_location()
            tags.add(one)
        return self

    def on_load(self, *args):
        return self.add_func_tags('load', *args)

    def on_tick(self, *args):
        return self.add_func_tags('tick', *args)
