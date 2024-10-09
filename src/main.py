import sys

from PySide6 import QtCore, QtWidgets, QtGui
from pymem import Pymem  # type: ignore
from pymem.exception import ProcessNotFound  # type: ignore

from game.world import World
from game.local_player import LocalPlayer
from datatypes import Vec3, Viewport
from world_to_screen import world_to_screen


process_name = "ac_client.exe"

try:
    process = Pymem(process_name)
except ProcessNotFound:
    print(f"Process {process_name} not found. Make sure Assault Cube is running.")
    exit()

player = LocalPlayer(process)
world = World(process)


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Set up the window.
        self.setWindowTitle("p1nkrat's AssaultCube trainer")
        self.setWindowIcon(QtGui.QIcon("logo.png"))
        self.layout = QtWidgets.QVBoxLayout(self)
        self.text = QtWidgets.QLabel(
            "p1nkrat's AssaultCube trainer", alignment=QtCore.Qt.AlignCenter
        )
        self.layout.addWidget(self.text)

        # Jump hack.
        self.jump_hack_enabled = False
        self.jump_hack_button = QtWidgets.QPushButton("🦘 Enable Jump Hack")
        self.jump_hack_button.clicked.connect(self.enable_jump_hack)
        self.layout.addWidget(self.jump_hack_button)

        # God mode.
        self.god_mode_enabled = False
        self.god_mode_button = QtWidgets.QPushButton("🦸 Enable God Mode")
        self.god_mode_button.clicked.connect(self.enable_god_mode)
        self.layout.addWidget(self.god_mode_button)

    @QtCore.Slot()
    def enable_jump_hack(self) -> None:
        if not self.jump_hack_enabled:
            world.enable_jump_hack()
            self.jump_hack_enabled = True
            self.text.setText("Jump hack enabled.")
        else:
            world.disable_jump_hack()
            self.jump_hack_enabled = False
            self.text.setText("Jump hack disabled.")

    @QtCore.Slot()
    def enable_god_mode(self) -> None:
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(400, 300)
    widget.show()

    sys.exit(app.exec())

# player.set_all_ammo(1337)
# player.set_heatlh(1337)
# player.set_armor(1337)
# player.set_position()


# Convert a 3D coordinate to a 2D screen coordinate.
# coords = Vec3(63.18, 5.1, 11)
# modelview_matrix = player.get_modelview_matrix()
# projection_matrix = player.get_projection_matrix()

# object_2d_coords = world_to_screen(
#     coords, modelview_matrix, projection_matrix, Viewport(0, 0, 3840, 2160)
# )

# print("💃🏻💃🏻💃🏻💃🏻")
# print(object_2d_coords)

# while True:
#     player.increase_speed()
