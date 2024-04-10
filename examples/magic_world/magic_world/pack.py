from mc_pack_builder import DataPack, Minecraft, ScoreBoard
from . import config

# the Minecraft namespace
mc = Minecraft()

# the DataPack instance
data_pack = DataPack("some convenient magic", 26)
# the datapack namespace
magic = data_pack.namespace("magic")
admin_guard = ScoreBoard(config.ADMIN_SCOREBOARD_NAME)

magic.on_load(admin_guard.add_objective(), *admin_guard.level_guard_cmds(config.ADMIN_LEVEL))
