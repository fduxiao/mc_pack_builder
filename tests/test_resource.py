import unittest
from mc_pack_builder import Minecraft


class TestResource(unittest.TestCase):
    def testResource(self):
        mc = Minecraft()
        sword = mc.item("diamond_sword")
        sword.enchant(mc.enchantments.sharpness())
        self.assertEqual(sword.as_str(),
                         'minecraft:diamond_sword{Enchantments: [{id: "minecraft:sharpness", lvl: 1}]}')

        book = mc.item("enchanted_book")
        book.enchant(mc.enchantments.mending())
        book.enchant(mc.enchantments.infinity())
        self.assertEqual(book.as_str(), 'minecraft:enchanted_book{'
                                        'Enchantments: [{'
                                        'id: "minecraft:mending", lvl: 1}, '
                                        '{id: "minecraft:infinity", lvl: 1}]}')


if __name__ == '__main__':
    unittest.main()
