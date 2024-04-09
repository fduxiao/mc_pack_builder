from mc_pack_builder import *
from . import weapons
from .pack import mc, magic


book_funcs = magic.functions.dir('books')


weapon_book = mc.written_book("Weapon Book", "xiao").pages(
    "This is a book that can give you some powerful weapons.",
    "Swords:\n" + Text("excalibur").color("blue").run_command(weapons.give_excalibur()),
)

give_weapon_book = book_funcs.new("weapon_book").body(give(at_s(), weapon_book))
