from mc_pack_builder.namespace import Namespace
from .enchantments import Enchantment


class Minecraft(Namespace):
    def __init__(self):
        super().__init__("minecraft")

    enchantments = Enchantment()
