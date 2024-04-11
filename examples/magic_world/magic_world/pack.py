from mc_pack_builder import DataPack, Minecraft, ScoreBoard
from . import config

# the Minecraft namespace
mc = Minecraft()

# the DataPack instance
data_pack = DataPack("some convenient magic", 26)
# the datapack namespace
magic_ns = data_pack.namespace("magic")
admin_guard = ScoreBoard(config.ADMIN_SCOREBOARD_NAME)

magic_ns.on_load(admin_guard.add_objective(), *admin_guard.level_guard_cmds(config.ADMIN_LEVEL))


trigger_group = magic_ns.functions.trigger_group('magic_func_trigger')
carrot_stick = magic_ns.functions.scoreboard_positive('carrot_stick', mc.used(mc.carrot_stick()))
