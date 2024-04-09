from mc_pack_builder import DataPack, Minecraft
from . import config

# the Minecraft namespace
mc = Minecraft()

# the DataPack instance
data_pack = DataPack("some convenient magic", 26)
# the datapack namespace
magic = data_pack.namespace("magic")
admin_guard = magic.level_guard(config.ADMIN_SCOREBOARD_NAME, config.ADMIN_LEVEL)
