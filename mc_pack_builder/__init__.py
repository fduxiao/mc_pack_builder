"""
Minecraft allows players to customize the game through resource packs and data packs.
But to write such a pack through minecraft command alone is not easy, especially when
you want to make an RPG game with a lot of enchant NBT tags to write.

In this package, I intend to use python as a code generator for that purpose.
There have already existed a lot of similar projects, but they are not aimed to do
designs on the high level. So I still invent the wheel again.
"""


from .pack import *
from .natural_model import *
from .data_pack import *
from .command import *
from .resources import *
from .json_text import *

from .minecraft import Minecraft
