#!/usr/bin/env python3
from mc_pack_builder import DataPack, Minecraft

# the Minecraft namespace
mc = Minecraft()

# the DataPack instance
data_pack = DataPack("some extra recipes", 26)
# the datapack namespace
extra_recipes = data_pack.namespace("extra_recipes")

# first we make some custom tags
wood = extra_recipes.tags.items("wood")
wood.add(mc.tag("logs"), mc.tag("planks"), mc.item("stick"))

hard = extra_recipes.tags.items("hard")
hard.add(wood, mc.item("cobble_stone"), mc.item("stone"))


# finally we write the data pack to a file
data_pack.write_to("./build/mc_extra_recipes")
