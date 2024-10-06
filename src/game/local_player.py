import numpy as np
from memory import find_dynamic_address


class LocalPlayer:

    class Offsets:
        local_player = 0x0017E0A8

        # Player status
        # Type: int
        health = 0xEC
        armor = 0xF0
        is_alive = 0x76  # 0 = dead, 1 = alive, 4 = in edit mode

        # Ammunition
        # Type: int
        assault_rifle_ammo = 0x140
        submachine_gun_ammo = 0x138
        sniper_ammo = 0x13C
        shotgun_ammo = 0x134
        carabine_ammo = 0x130
        pistol_ammo = 0x12C
        grenade_ammo = 0x144

        # Fire rate
        # Type: byte
        carabine_fire_rate = 0x155
        shotgun_fire_rate = 0x159
        submachine_fire_rate = 0x15D
        sniper_fire_rate = 0x161

        # Position
        # Type: float
        x_position = 0x28
        y_position = 0x2C
        z_position = 0x30

        # Velocity
        # Type: float
        x_velocity = 0x10
        y_velocity = 0x14
        z_velocity = 0x18

        # Movement
        # Type: single byte
        forward_movement_enabled = 0x74  # 1 = forward, 255 = backwards
        side_movement_enabled = 0x75  # 1 = left, 255 = right

        # Camera
        # Type: float
        x_camera = 0x34
        y_camera = 0x38

    def __init__(self, process) -> None:
        self.process = process
        self.base_address = process.base_address + self.Offsets.local_player

    def set_ammo(self, ammo_offset: int, value: int) -> None:
        address = find_dynamic_address(
            self.process.process_handle,
            self.base_address,
            [ammo_offset],
            32,
        )
        self.process.write_int(address, value)

    def set_all_ammo(self, value: int = 1337) -> None:
        ammo_offsets = [
            self.Offsets.assault_rifle_ammo,
            self.Offsets.submachine_gun_ammo,
            self.Offsets.sniper_ammo,
            self.Offsets.shotgun_ammo,
            self.Offsets.pistol_ammo,
            self.Offsets.grenade_ammo,
        ]

        for offset in ammo_offsets:
            self.set_ammo(offset, value)

    def set_heatlh(self, value: int) -> None:
        address = find_dynamic_address(
            self.process.process_handle,
            self.base_address,
            [self.Offsets.health],
            32,
        )
        self.process.write_int(address, value)

    def set_armor(self, value: int) -> None:
        address = find_dynamic_address(
            self.process.process_handle,
            self.base_address,
            [self.Offsets.armor],
            32,
        )
        self.process.write_int(address, value)

    def set_position(self) -> None:
        address_x = find_dynamic_address(
            self.process.process_handle,
            self.base_address,
            [self.Offsets.x_position],
            32,
        )
        self.process.write_float(address_x, 150.0)

    def get_modelview_matrix(self) -> np.ndarray:
        # Address is static, so we use it directly
        address = 0x0057DF90

        # Reading 16 floats (4x4 matrix)
        matrix_values = []
        for i in range(16):
            matrix_value = self.process.read_float(
                address + i * 4
            )  # 32-bit float, 4 bytes each
            matrix_values.append(matrix_value)

        # Reshape the list of values into a 4x4 matrix
        modelview_matrix = np.array(matrix_values).reshape((4, 4))
        return modelview_matrix

    def get_projection_matrix(self) -> np.ndarray:
        # Address is static, so we use it directly
        address = 0x0057DFD0

        # Reading 16 floats (4x4 matrix)
        matrix_values = []
        for i in range(16):
            matrix_value = self.process.read_float(
                address + i * 4
            )  # 32-bit float, 4 bytes each
            matrix_values.append(matrix_value)

        # Reshape the list of values into a 4x4 matrix
        modelview_matrix = np.array(matrix_values).reshape((4, 4))
        return modelview_matrix

    def increase_speed(self) -> None:
        multiplier = 2.0

        x_velocity_address = find_dynamic_address(
            self.process.process_handle,
            self.base_address,
            [self.Offsets.x_velocity],
            32,
        )
        value = self.process.read_float(x_velocity_address)
        self.process.write_float(x_velocity_address, value * multiplier)

        y_velocity_address = find_dynamic_address(
            self.process.process_handle,
            self.base_address,
            [self.Offsets.y_velocity],
            32,
        )
        value = self.process.read_float(y_velocity_address)
        self.process.write_float(y_velocity_address, value * multiplier)

        z_velocity_address = find_dynamic_address(
            self.process.process_handle,
            self.base_address,
            [self.Offsets.z_velocity],
            32,
        )
        value = self.process.read_float(z_velocity_address)
        self.process.write_float(z_velocity_address, value * multiplier)
