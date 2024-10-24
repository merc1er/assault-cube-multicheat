import math
from pyMeow import vec2, vec3

from entity import Entity


def calculate_angles(local_pos: vec3, enemy_pos: vec3) -> vec2:
    # Calculate differences in position
    delta_x = enemy_pos["x"] - local_pos["x"]
    delta_y = enemy_pos["y"] - local_pos["y"]
    delta_z = enemy_pos["z"] - local_pos["z"]

    # Calculate yaw (horizontal angle)
    yaw = math.degrees(math.atan2(delta_y, delta_x)) + 90.0

    # Calculate the distance in the 2D plane
    distance = math.hypot(delta_x, delta_y)

    # Calculate pitch (vertical angle)
    pitch = -math.degrees(math.atan2(-delta_z, distance))

    return pitch, yaw


def aim_at_enemy(local_player: Entity, enemy_entity: Entity) -> None:
    pitch, yaw = calculate_angles(local_player.feet_pos3d, enemy_entity.feet_pos3d)
    local_player.set_view_angles(pitch, yaw)
