import unittest
from mc_pack_builder import Minecraft
from mc_pack_builder import command as cmd

at = cmd.at
mc = Minecraft()


def make_sword():
    return mc.item("diamond_sword").unbreakable()


class TestCommand(unittest.TestCase):
    def test_target_selector(self):
        self.assertEqual(str(at('e')(type='item')
                             .nbt(Item=make_sword().item_nbt(False))),
                         '@e[type=item,nbt={Item: {id: "minecraft:diamond_sword", tags: {Unbreakable: 1}}}]')

    def test_give(self):
        sword = make_sword().enchant(mc.enchantments.sharpness(10))
        give = cmd.give(at('s'), sword, 2)
        self.assertEqual(str(give),
                         'give @s minecraft:diamond_sword'
                         '{Unbreakable: 1, Enchantments: [{id: "minecraft:sharpness", lvl: 10}]} 2')


if __name__ == '__main__':
    unittest.main()
