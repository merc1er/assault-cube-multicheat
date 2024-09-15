import numpy as np


class ViewMatrix:
    offset = 0x17DFFC


class Vec2:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y


class Vec3:
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z


class Viewport:
    def __init__(self, x: float, y: float, width: float, height: float) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height


def world_to_screen(
    world_coords: Vec3,
    modelview_matrix: np.ndarray,
    projection_matrix: np.ndarray,
    viewport: Viewport,
) -> Vec2 | None:
    """
    Transforms world coordinates to screen coordinates.

    Parameters:
        world_coords: A Vec3 object containing (x, y, z) world coordinates.
        modelview_matrix: A 4x4 numpy array representing the modelview matrix.
        projection_matrix: A 4x4 numpy array representing the projection matrix.
        viewport: A Viewport object defining the viewport (x, y, width, height).

    Returns:
        A Vec2 object of (screen_x, screen_y) screen coordinates, or None if the point cannot be projected.
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
