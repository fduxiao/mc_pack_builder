from ..pack import Pack
from ..natural_model import DictModel, Field


class MCMeta(DictModel):
    desc = Field("pack/description")
    format = Field("pack/pack_format")


class DataPack(Pack):
    def __init__(self, desc: str, pack_format: int):
        super().__init__()
        self.mcmeta: MCMeta = self.add_json("pack.mcmeta", MCMeta())
        self.mcmeta.desc = desc
        self.mcmeta.format = pack_format
