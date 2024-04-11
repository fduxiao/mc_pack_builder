from mc_pack_builder import *
from .pack import mc, magic_ns


weapons_funcs = magic_ns.functions.dir("weapons")

weapon_book = mc.written_book("Weapon Book", "xiao").pages(
    "This is a book that can give you some powerful weapons."
)


excalibur_enchantments = [mc.enchantments.sharpness(10)]
excalibur = (mc.item("diamond_sword")
             .enchant(*excalibur_enchantments)
             .unbreakable()
             .display_name(Text("excalibur").color("red"))
             .lore("The master sword in the legend.")
             .lore("It never gets worn."))

weapon_book.pages(
    "Swords:\n" + Text("excalibur").color("blue").run_command(give(at_s(), excalibur)),
)
