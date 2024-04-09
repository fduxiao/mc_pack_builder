from mc_pack_builder import *
from .pack import mc, magic


weapons_funcs = magic.functions.dir("weapons")


excalibur_enchantments = [mc.enchantments.sharpness(10)]
excalibur = (mc.item("diamond_sword")
             .enchant(*excalibur_enchantments)
             .unbreakable()
             .display_name(Text("excalibur").color("red"))
             .lore("The master sword in the legend.")
             .lore("It never gets worn."))


give_excalibur = weapons_funcs.new('excalibur').body(give(at_s(), excalibur))
