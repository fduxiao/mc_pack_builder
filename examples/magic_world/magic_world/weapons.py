from mc_pack_builder import *
from .pack import mc, magic


weapons_funcs = magic.functions.dir("weapons")


excalibur = (mc.item("diamond_sword")
             .enchant(mc.enchantments.sharpness(10))
             .unbreakable()
             .display_name(Text("excalibur").color("red"))
             .lore("The master sword in the legend.")
             .lore("It never gets worn."))


give_excalibur = weapons_funcs.new('excalibur').body(give(at_s(), excalibur))
