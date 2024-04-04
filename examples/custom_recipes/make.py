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
hard.add(wood, mc.item("cobblestone"), mc.item("stone"))

# then we are able to add some recipes based on them
recipes = extra_recipes.recipes
recipes.crafting_shaped('pickaxe').result(mc.item("stone_pickaxe")).define(
    ["HHH",
     " W ",
     " W "],
    **{'W': wood, 'H': hard}
)

recipes.crafting_shapeless('black_dye').result(mc.item('black_dye'), 3).define(
    [mc.item("coal"), mc.item("charcoal")]
)

recipes.stone_cutting('sand').define(mc.item('gravel')).result(mc.item("sand"), 1)

recipes.add_json('gravel.json', {
    "type": "stonecutting",
    "ingredient": {
        "item": "minecraft:cobblestone"
    },
    "result": "minecraft:gravel",
    "count": 4
})


# finally we write the data pack to a file
data_pack.write_to("./build/mc_extra_recipes")
