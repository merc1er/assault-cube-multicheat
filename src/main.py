from pymem import Pymem  # type: ignore
import numpy as np

from cheats import Player
from datatypes import Vec3, Viewport
from world_to_screen import world_to_screen


process = Pymem("ac_client.exe")
player = Player(process)
player.set_all_ammo(1337)
player.set_heatlh(1337)
player.set_armor(1337)
# player.set_position()


# Convert a 3D coordinate to a 2D screen coordinate.
coords = Vec3(123.5736542, 139.7576294, -5.0)
modelview_matrix = np.array(
    [
        [-0.55, 0.84, 0.00, 0.00],
        [0.15, 0.10, 0.53, 0.00],
        [-325.11, -466.54, 1.67, -3.33],
        [325.94, 467.11, -1.99, 3.33],
    ]
)
projection_matrix = np.array(
    [
        [-0.55, 0.48, 0.79, 0.79],
        [0.84, 0.31, 0.52, 0.52],
        [0.00, 1.68, -0.32, -0.32],
        [-64.18, -90.21, -150.03, -149.71],
    ]
)
object_2d_coords = world_to_screen(
    coords, modelview_matrix, projection_matrix, Viewport(0, 0, 3840, 2160)
)

print("💃🏻💃🏻💃🏻💃🏻")
print(object_2d_coords)
