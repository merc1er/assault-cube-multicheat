import pyMeow as pm
from pointers import LOCAL_PLAYER


class Entity:

    class Offsets:
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

    def __init__(self, process, base_address) -> None:
        self.process = process
        self.base_address = base_address
        self.local_player_address = pm.r_int(process, base_address + LOCAL_PLAYER)

    def set_all_ammo(self) -> None:
        ammo_offsets = [
            self.Offsets.assault_rifle_ammo,
            self.Offsets.submachine_gun_ammo,
            self.Offsets.sniper_ammo,
            self.Offsets.shotgun_ammo,
            self.Offsets.pistol_ammo,
            self.Offsets.grenade_ammo,
        ]

        for offset in ammo_offsets:
            pm.w_int(self.process, self.local_player_address + offset, 1337)

    def set_heatlh(self) -> None:
        pm.w_int(self.process, self.local_player_address + self.Offsets.health, 1337)
