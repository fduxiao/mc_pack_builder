from mc_pack_builder.resources import enchantment


class Enchantment:
    @staticmethod
    def enchantment(name, lvl=1):
        return enchantment(f"minecraft:{name}", lvl)

    def sharpness(self, lvl=1):
        return self.enchantment("sharpness", lvl)

    def mending(self):
        return self.enchantment("mending")

    def infinity(self):
        return self.enchantment("infinity")
