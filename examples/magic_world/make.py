#!/usr/bin/env python3
from mc_pack_builder import command as cmd
# The datapack magic_world can be made into a package.
# You can directly use it, or you can make some further
# modification. If you don't like the idea of export an
# instance, you can always make a class instead.
from magic_world import config, MagicWorld

# change some config if you want
config.ADMIN_LEVEL = 9

# Then load the content
magic_world = MagicWorld()


# some modifications if you want
@magic_world.magic.functions.new()
@magic_world.admin_guard.level_guard(3)
def f3():
    yield cmd.say("I am f3.")


magic_world.magic.on_load(cmd.tell("@a", "on load"))
magic_world.weapons.excalibur_enchantments[0].lvl(11)


if __name__ == '__main__':
    # save to file
    magic_world.data_pack.write_to('build/magic')
