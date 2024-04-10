#!/usr/bin/env python3
from mc_pack_builder import command as cmd
# The datapack magic_world can be made into a package.
# You can directly use it, or you can make some further
# modification. If you don't like the idea of export an
# instance, you can always make a class instead.
from magic_world import data_pack, magic, admin_guard, config, weapons


# change some config if you want
config.ADMIN_LEVEL.data = 9


# some modifications if you want
@magic.functions.new()
@admin_guard.level_guard(3)
def f3():
    yield cmd.say("I am f3.")


magic.on_load(cmd.tell("@a", "on load"))
weapons.excalibur_enchantments[0].lvl(11)


if __name__ == '__main__':
    # save to file
    data_pack.write_to('build/magic')
