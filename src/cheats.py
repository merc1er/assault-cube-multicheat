from memory import find_dynamic_address


class Player:
    class Offsets:
        local_player = 0x0017E0A8

        health = 0xEC
        armor = 0xF0

        assault_rifle_ammo = 0x140
        submachine_gun_ammo = 0x138
        sniper_ammo = 0x13C
        shotgun_ammo = 0x134
        pistol_ammo = 0x12C
        grenade_ammo = 0x144

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
