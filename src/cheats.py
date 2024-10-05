import numpy as np
from memory import find_dynamic_address


class GameMemory:

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

        # Jump code
        jump_code_start = 0xC2486

    def __init__(self, process) -> None:
        self.process = process
        self.base_address = process.base_address + self.Offsets.local_player

    def jump_higher(self) -> None:
        address = self.process.base_address + 0xC2486
        allocated_memory = self.process.allocate(2048)

        # The assembly instructions translated to their hex equivalent.
        # This will mov [esi + 18], 40A00000 (which is 5 in float) and then jump to the
        # original code.
        new_code = [
            0xC7,
            0x46,
            0x18,
            0x00,
            0x00,
            0xA0,
            0x40,  # mov [esi+18],40A00000 (5.0 in float)
            0xE9,
            0x00,
            0x00,
            0x00,
            0x00,  # jmp exit (the relative address will be filled in later)
        ]

        # Calculate the jump back address for returnhere
        # Distance from the allocated memory to "ac_client.exe" + C2486 + 7 (size of
        # original code + NOPs)
        return_address = (address + 7) - (allocated_memory + len(new_code))

        # Patch the jump address into the new code (E9 uses a relative address for the
        # jump)
        new_code[-4:] = return_address.to_bytes(4, byteorder="little", signed=True)

        # Write the new code to the allocated memory
        self.process.write_bytes(allocated_memory, bytes(new_code), len(new_code))

        # Patch the original code at "ac_client.exe" + C2486 to jump to the allocated
        # memory
        jmp_newmem = (
            b"\xE9"
            + (allocated_memory - address - 5).to_bytes(
                4, byteorder="little", signed=True
            )
            + b"\x90\x90"
        )
        self.process.write_bytes(address, jmp_newmem, len(jmp_newmem))

        print(
            f"Memory at {hex(address)} patched to jump to allocated memory at {hex(allocated_memory)}"
        )

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
