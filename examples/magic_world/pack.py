from mc_pack_builder import DataPack, Minecraft


# the Minecraft namespace
mc = Minecraft()

# the DataPack instance
data_pack = DataPack("some convenient magic", 26)
# the datapack namespace
magic = data_pack.namespace("magic")
