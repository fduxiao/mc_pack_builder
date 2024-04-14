from mc_pack_builder import *
from .pack import trigger_group, mc, carrot_stick, magic_ns


magics = magic_ns.functions.dir('magics')
magics_trigger = trigger_group.dir("magics")

magic_book = mc.written_book('MagicBook', 'xiao')
magic_book.pages(
    "Fancy Magics\n"
    "You can also use them by trigger command."
)


@magics_trigger.new()
def fireball():
    yield summon(mc.item('fireball').resource_location(), '^ ^1 ^2', '{ExplosionPower: 5}')


magic_book.pages(
    "Fireballs:\n\n" +
    Text("fireball1").color('red').run_command(fireball.trigger())
)


# the next is the scroll system
# we have to use an item modifier to remove a scroll

remove1 = (magic_ns.item_modifiers.new('magics/remove1')
           .function(mc.item_modifier_functions.set_count)
           .count(-1).add())


class Scroll(Item):
    scrolls: list["Scroll"] = []

    def __init__(self, name: str, color='black', desc="", custom_id=None, consume=True):
        super().__init__('paper', 'minecraft')
        if custom_id is None:
            custom_id = name.replace(' ', '_')
        self.custom_id(custom_id)
        self.display_name(Text(name).color(color)).lore(desc)
        self.commands = []
        self.name = name
        self.color = color
        self.desc = desc
        type(self).scrolls.append(self)
        self.consume = consume

    @property
    def line(self):
        return Text(self.name).color(self.color).run_command(give(at_s(), self, 64)) + ": " + self.desc

    def set_cmd(self, *cmds):
        self.commands = cmds
        return self

    def execute(self):
        for cmd in self.commands:
            yield execute().if_entity(at_s().selected_item(self)).run(cmd)
        if self.consume:
            yield execute().if_entity(at_s().selected_item(self)).run(
                f'item modify entity @s weapon.mainhand {remove1}'
            )


# make scroll that can be used by a carrot_stick
magic_book.pages(Text("The following are available scrolls.\n\n"))

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


magic_book.pages(
    "attacking magics:\n\n" +
    fire_scroll.line + '\n\n' +
    lightning_scroll.line + '\n\n' +
    arrow_scroll.line
)

# make a teleport scroll
# to use it, we have to throw a position scroll nearby
# and use the locator scroll. Then the position scroll nearby will
# record the coordinate and be turned into a teleport scroll.

# first make a position scroll
position_scroll = Scroll('position scroll', color="green", desc="throw it nearby and use a locator scroll",
                         consume=False)
position_scroll.lore(0, 0, 0)
position_scroll.set_cmd(
    "tell @s throw it on the ground and use a locator scroll"
)

# then the locator scroll
locator_scroll = Scroll('locator scroll', color="green",
                        desc="it turns nearby position scrolls (at most 5) to a teleport scroll")


def make_teleport_scroll(x, y=None, z=None):
    if y is None and z is None:
        x, y, z = x
    scroll = Scroll('teleport scroll', color="green", desc="teleport to position")
    scroll.lore(x, y, z)
    return scroll


teleport_scroll = make_teleport_scroll(0, 0, 0)


@magics.new()
def store_to_position_scroll():
    # store coordinate to nbt
    yield 'data modify entity @s Item.tag.TargetPos set from entity @p Pos'
    yield 'data modify entity @s Item.tag.TargetRotation set from entity @p Rotation'
    # I will not change the name in case you want to rename it by an anvil.
    # yield f"data modify entity @s Item.tag.display.Name set value '{teleport_scroll.display.display_name}'"
    # set and id
    yield 'data modify entity @s Item.tag.CustomID set value teleport_scroll'
    yield f"data modify entity @s Item.tag.display.Lore[0] set value '{teleport_scroll.display.lore[0]}'"
    yield 'data modify entity @s Item.tag.display.Lore[1] set string entity @s Pos[0]'
    yield 'data modify entity @s Item.tag.display.Lore[2] set string entity @s Pos[1]'
    yield 'data modify entity @s Item.tag.display.Lore[3] set string entity @s Pos[2]'
    # add coordinate to lore
    # notify nearby player
    yield 'tell @p position stored'


locator_scroll.set_cmd(
    execute().as_(at_e().type(mc.type.item).limit(5).item(position_scroll)).align().run(store_to_position_scroll())
)

PosX = magic_ns.scoreboard("PosX")
PosY = magic_ns.scoreboard("PosY")
PosZ = magic_ns.scoreboard("PosZ")


@magics.new()
def armor_stand_tp():
    # executed at the position of the player holding the scroll
    # when @s is the specific armor stand and @p is the target player
    yield 'data modify entity @s Pos set from entity @p SelectedItem.tag.TargetPos'
    yield 'data modify entity @s Rotation set from entity @p SelectedItem.tag.TargetRotation'
    # I am not sure which is the nearest, so I checked with chicken
    # yield 'execute as @s run tp @e[type=minecraft:chicken,limit=1,sort=nearest] @s'
    yield 'execute as @s run tp @p @s'


@magics.new()
def teleport_to_scroll():
    yield 'summon armor_stand ~ ~ ~ {NoGravity:1b,Invulnerable:1b,Invisible:1b,Tags:["teleport"]}'
    stand = at_e(tag='teleport').limit(1).sort('nearest').type(mc.type.armor_stand)
    # execute as the armor stand
    yield execute().at(at_s()).as_(stand).run(armor_stand_tp())
    yield "kill @e[type=minecraft:armor_stand,tag=teleport]"
    yield 'tell @s teleported'


teleport_scroll.set_cmd(teleport_to_scroll())


magic_book.pages(
    "Teleporting magics:\n\n" +
    position_scroll.line + '\n\n' +
    locator_scroll.line + '\n\n'
)


@carrot_stick.new()
def magic_carrot_call():
    for one in Scroll.scrolls:
        yield from one.execute()
