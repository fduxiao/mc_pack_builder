from mc_pack_builder import *
from .pack import data_pack, magic_ns


some_property = scoreboard("some_property")
magic_ns.on_load(some_property.add_objective())
