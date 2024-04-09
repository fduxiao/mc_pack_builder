from mc_pack_builder import *
from .pack import data_pack, magic


run_level = scoreboard("run_level")
magic.on_load(run_level.add_objective())
