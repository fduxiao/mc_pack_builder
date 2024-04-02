#!/usr/bin/env python3
from mc_pack_builder import DataPack


data_pack = DataPack("some extra recipes", 26)
data_pack.write_to("./mc_extra_recipes")
