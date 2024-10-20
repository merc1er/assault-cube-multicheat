import pyMeow as pm


class Colors:
    blue = pm.get_color("blue")
    red = pm.get_color("red")
    pink = pm.get_color("pink")
    white = pm.get_color("white")
    black = pm.get_color("black")


class Entity:

    class Offsets:
        # Player status
        # Type: int
        health = 0xEC
        armor = 0xF0
        is_alive = 0x76  # 0 = dead, 1 = alive, 4 = in edit mode
        team = 0x30C

        name = 0x205

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
        pos = 0x4
        fpos = 0x28

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

    def __init__(self, process, address: int) -> None:
        self.process = process
        self.address = address
        self.health = pm.r_int(process, address + self.Offsets.health)
        if self.health <= 0:
            raise Exception("Entity is not alive.")
        self.name = pm.r_string(process, address + self.Offsets.name)
        self.team = pm.r_int(process, address + self.Offsets.team)
        self.pos3d = pm.r_vec3(process, address + self.Offsets.pos)
        self.fpos3d = pm.r_vec3(process, address + self.Offsets.fpos)
        self.pos2d = self.fpos2d = None
        self.head = self.width = self.center = None

    def get_team(self) -> int:
        return pm.r_int(self.process, self.address + self.Offsets.team)

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
            pm.w_int(self.process, self.address + offset, 1337)

    def set_heatlh(self) -> None:
        pm.w_int(self.process, self.address + self.Offsets.health, 1337)

    def world_to_screen(self, vm):
        try:
            self.pos2d = pm.world_to_screen(vm, self.pos3d)
            self.fpos2d = pm.world_to_screen(vm, self.fpos3d)
            self.head = self.fpos2d["y"] - self.pos2d["y"]
            self.width = self.head / 2
            self.center = self.width / 2
            return True
        except:
            return False

    def draw_box(self, local_player_team: int):
        color = Colors.red
        if local_player_team == self.team:
            color = pm.fade_color(Colors.blue, 0.3)
        pm.draw_rectangle(
            posX=self.pos2d["x"] - self.center,
            posY=self.pos2d["y"] - self.center / 2,
            width=self.width,
            height=self.head + self.center / 2,
            color=pm.fade_color(color, 0.3),
        )
        pm.draw_rectangle_lines(
            posX=self.pos2d["x"] - self.center,
            posY=self.pos2d["y"] - self.center / 2,
            width=self.width,
            height=self.head + self.center / 2,
            color=color,
            lineThick=1.2,
        )

    def draw_name(self):
        text_size = pm.measure_text(self.name, 15) / 2
        pm.draw_text(
            text=self.name,
            posX=self.pos2d["x"] - text_size,
            posY=self.pos2d["y"],
            fontSize=15,
            color=Colors.white,
        )

    def draw_health(self):
        text_size = pm.measure_text(f"{self.health} HP", 22) / 2
        color = Colors.pink if self.health < 50 else Colors.white
        pm.draw_text(
            text=f"{self.health} HP",
            posX=self.pos2d["x"] - text_size,
            posY=self.pos2d["y"] + 20,
            fontSize=22,
            color=color,
        )
