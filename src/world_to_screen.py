import numpy as np
from datatypes import Vec2, Vec3, Viewport


class ViewMatrix:
    offset = 0x17DFFC


def world_to_screen(
    world_coords: Vec3,
    modelview_matrix: np.ndarray,
    projection_matrix: np.ndarray,
    viewport: Viewport,
) -> Vec2 | None:
    """
    Transforms world coordinates to screen coordinates.
    """
    # Convert world coordinates to homogeneous coordinates
    world_coords_homogeneous = np.array(
        [world_coords.x, world_coords.y, world_coords.z, 1.0]
    )

    # Transform to clip coordinates
    clip_coords = projection_matrix @ (modelview_matrix @ world_coords_homogeneous)

    # Avoid division by zero
    if clip_coords[3] == 0.0:
        return None

    # Perform perspective division to get normalized device coordinates (NDC)
    ndc = clip_coords[:3] / clip_coords[3]

    # Map NDC to window coordinates
    screen_x = ((ndc[0] + 1) * 0.5 * viewport.width) + viewport.x
    screen_y = ((1 - ndc[1]) * 0.5 * viewport.height) + viewport.y

    return Vec2(screen_x, screen_y)
