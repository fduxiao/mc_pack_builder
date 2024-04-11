from mc_pack_builder import *
from . import weapons, magics
from .pack import trigger_group


book_funcs = trigger_group.dir('books')


@book_funcs.new()
def give_weapon_book():
    yield give(at_s(), weapons.weapon_book)


@book_funcs.new()
def give_magic_book():
    yield give(at_s(), magics.magic_book)
