from pymem import Pymem  # type: ignore
from pymem.exception import ProcessNotFound  # type: ignore

from cheats import GameMemory
from datatypes import Vec3, Viewport
from world_to_screen import world_to_screen


process_name = "ac_client.exe"

try:
    process = Pymem(process_name)
except ProcessNotFound:
    print(f"Process {process_name} not found. Make sure Assault Cube is running.")
    exit()

player = GameMemory(process)
player.jump_higher()

# player.set_all_ammo(1337)
# player.set_heatlh(1337)
# player.set_armor(1337)
# player.set_position()


# Convert a 3D coordinate to a 2D screen coordinate.
# coords = Vec3(63.18, 5.1, 11)
# modelview_matrix = player.get_modelview_matrix()
# projection_matrix = player.get_projection_matrix()

# object_2d_coords = world_to_screen(
#     coords, modelview_matrix, projection_matrix, Viewport(0, 0, 3840, 2160)
# )

# print("💃🏻💃🏻💃🏻💃🏻")
# print(object_2d_coords)

# while True:
#     player.increase_speed()
