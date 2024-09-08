class ViewMatrix:
    offset = 0x17DFFC


class Vec3:
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z


class Vec4:
    def __init__(self, x: float, y: float, z: float, w: float) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.w = w


def world_to_screen(
    positions: Vec3,
    screen: Vec3,
    matrix: list[float],
    window_width: int,
    window_height: int,
) -> bool:
    # Matrix-vector product, multiplying world (eye) coordinates by
    # projection matrix = clipCoords
    clip_coords = Vec4(
        positions.x * matrix[0]
        + positions.y * matrix[4]
        + positions.z * matrix[8]
        + matrix[12],
        positions.x * matrix[1]
        + positions.y * matrix[5]
        + positions.z * matrix[9]
        + matrix[13],
        positions.x * matrix[2]
        + positions.y * matrix[6]
        + positions.z * matrix[10]
        + matrix[14],
        positions.x * matrix[3]
        + positions.y * matrix[7]
        + positions.z * matrix[11]
        + matrix[15],
    )

    if clip_coords.w < 0.1:
        return False

    # Perspective division, dividing by clip.w = Normalized Device Coordinates
    normalized_device_coords = Vec3(
        clip_coords.x / clip_coords.w,
        clip_coords.y / clip_coords.w,
        clip_coords.z / clip_coords.w,
    )

    # Transform to window coordinates
    screen.x = (window_width / 2 * normalized_device_coords.x) + (
        normalized_device_coords.x + window_width / 2
    )
    screen.y = -(window_height / 2 * normalized_device_coords.y) + (
        normalized_device_coords.y + window_height / 2
    )

    return True
