import math
from pyMeow import vec2, vec3

from entity import Entity


def lerp(current: float, target: float, smoothing: float) -> float:
    """
    Linearly interpolate between current and target with a given smoothing factor.
    """

    return current + (target - current) / smoothing


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


def aim_at_enemy(
    local_player: Entity, enemy_entity: Entity, smoothing: float = 2.0
) -> None:
    # Calculate target pitch and yaw
    target_pitch, target_yaw = calculate_angles(
        local_player.feet_pos3d, enemy_entity.feet_pos3d
    )

    # Get current view angles
    current_pitch, current_yaw = local_player.get_view_angles()

    # Apply smoothing using linear interpolation
    smoothed_pitch = lerp(current_pitch, target_pitch, smoothing)
    smoothed_yaw = lerp(current_yaw, target_yaw, smoothing)

    # Set the smoothed view angles
    local_player.set_view_angles(smoothed_pitch, smoothed_yaw)
