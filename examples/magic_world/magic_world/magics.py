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
line = Text("The following are available scrolls.\n\n")

fire_scroll = mc.paper().custom_id('fire_scroll').display_name(Text('fire scroll').color('red'))
line += Text('fire scroll').color('red').run_command(give(at_s(), fire_scroll, 10)) + ": summon a fire ball"

magic_book.pages(line)


@carrot_stick.new()
def magic_carrot_call():
    yield execute().if_entity(at_s().selected_item(fire_scroll)).run(fireball())
    yield execute().if_entity(at_s().selected_item(fire_scroll)).run(clear('@s', fire_scroll.custom_id(), 1))
