from pymem import Pymem  # type: ignore
from cheats import Player


process = Pymem("ac_client.exe")
player = Player(process)
player.set_all_ammo(1337)
player.set_heatlh(1337)
player.set_armor(1337)
