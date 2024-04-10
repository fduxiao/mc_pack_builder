from . import config


class MagicWorld:
    def __init__(self):
        from .pack import data_pack, magic, admin_guard
        from . import functions
        from . import books
        from . import players
        from . import weapons

        self.data_pack = data_pack
        self.magic = magic
        self.admin_guard = admin_guard
        self.functions = functions
        self.books = books
        self.players = players
        self.weapons = weapons
