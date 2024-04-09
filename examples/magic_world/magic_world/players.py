from mc_pack_builder import *
from .pack import data_pack, magic


some_property = scoreboard("some_property")
magic.on_load(some_property.add_objective())
