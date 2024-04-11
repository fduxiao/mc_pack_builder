from mc_pack_builder import *
from .pack import trigger_group, mc, carrot_stick


magics = trigger_group.dir("magics")

magic_book = mc.written_book('MagicBook', 'xiao')
magic_book.pages(
    "Fancy Magics\n"
    "You can also use them by trigger command."
)


@magics.new()
def fireball():
    yield summon(mc.item('fireball').resource_location(), '^ ^1 ^2', '{ExplosionPower: 2}')


magic_book.pages(
    "Fireballs:\n\n" +
    Text("fireball1").color('red').run_command(fireball.trigger())
)


# make scroll that can be used by a carrot_stick


@carrot_stick.new()
def carrot_call():
    yield tell(at_s(), 'used')
