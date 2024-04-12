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
    yield summon(mc.item('fireball').resource_location(), '^ ^1 ^2', '{ExplosionPower: 5}')


magic_book.pages(
    "Fireballs:\n\n" +
    Text("fireball1").color('red').run_command(fireball.trigger())
)


class Scroll(Item):
    scrolls: list["Scroll"] = []

    def __init__(self, name: str, color='black', desc="", custom_id=None):
        super().__init__('paper', 'minecraft')
        if custom_id is None:
            custom_id = name.replace(' ', '_')
        self.custom_id(custom_id)
        self.display_name(Text(name).color(color)).lore(desc)
        self.commands = []
        self.line = Text(name).color(color).run_command(give(at_s(), self, 10)) + ": " + desc
        type(self).scrolls.append(self)

    def set_cmd(self, *cmds):
        self.commands = cmds
        return self

    def execute(self):
        for cmd in self.commands:
            yield execute().if_entity(at_s().selected_item(self)).run(cmd)
        yield execute().if_entity(at_s().selected_item(self)).run(clear('@s', self.custom_id(), 1))


# make scroll that can be used by a carrot_stick
line = Text("The following are available scrolls.\n\n")

fire_scroll = Scroll('fire scroll', 'red', 'summon a fire ball')
fire_scroll.set_cmd(fireball())
lightning_scroll = Scroll('lightning scroll', 'blue', 'summon a lighting bolt')
lightning_scroll.set_cmd(
    *(f'summon minecraft:lightning_bolt ^ ^ ^{i}' for i in range(6, 11)),
    *(f'summon minecraft:lightning_bolt ^ ^ ^{i}' for i in range(6, 11)),
    *(f'summon minecraft:lightning_bolt ^ ^ ^{i}' for i in range(6, 11)),
)
arrow_scroll = Scroll('arrow scroll', 'gray', 'summon a rain of arrows')
arrow_nbt = '{Potion:"minecraft:strong_harming"}'


@magics.new()
def rain_arrows():
    for i in range(-4, 4):
        for j in range(0, 8):
            yield f'summon minecraft:arrow ^{i / 2} ^10 ^{8 + j / 2} {arrow_nbt}'


arrow_scroll.set_cmd(rain_arrows())


for scroll in Scroll.scrolls:
    line += scroll.line + '\n\n'

magic_book.pages(line)


@carrot_stick.new()
def magic_carrot_call():
    for one in Scroll.scrolls:
        yield from one.execute()
