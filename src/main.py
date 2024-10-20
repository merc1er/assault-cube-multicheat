import sys

from PySide6 import QtCore, QtWidgets, QtGui
import pyMeow as pm

from config import process, base_address
from entity import Entity
from world import World
from pointers import ENTITY_LIST, PLAYER_COUNT, VIEW_MATRIX, LOCAL_PLAYER


player = Entity(process=process, address=pm.r_int(process, base_address + LOCAL_PLAYER))
world = World()


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

        # Increase health.
        self.increase_health_button = QtWidgets.QPushButton("❤️‍🩹 Increase health")
        self.increase_health_button.clicked.connect(player.set_heatlh)
        self.layout.addWidget(self.increase_health_button)

        # Increase ammo.
        self.increase_ammo_button = QtWidgets.QPushButton("⬆️ Increase ammo")
        self.increase_ammo_button.clicked.connect(player.set_all_ammo)
        self.layout.addWidget(self.increase_ammo_button)

        # Enable jump hack.
        self.enable_jump_hack_button = QtWidgets.QPushButton("🦘 Enable jump hack")
        self.enable_jump_hack_button.clicked.connect(world.enable_jump_hack)
        self.layout.addWidget(self.enable_jump_hack_button)


class OverlayThread(QtCore.QThread):
    """
    Custom thread to run the while loop in the background.
    """

    def run(self):
        pm.overlay_init(target="AssaultCube", fps=60, trackTarget=True)
        while pm.overlay_loop():
            pm.begin_drawing()
            pm.draw_fps(10, 10)
            local_player_team = player.get_team()
            player_count = pm.r_int(process, base_address + PLAYER_COUNT)
            if player_count > 1:
                ent_buffer = pm.r_ints(
                    process, pm.r_int(process, base_address + ENTITY_LIST), player_count
                )[1:]
                v_matrix = pm.r_floats(process, base_address + VIEW_MATRIX, 16)
                for address in ent_buffer:
                    try:
                        ent = Entity(process, address)
                        if ent.world_to_screen(v_matrix):
                            ent.draw_box(local_player_team)
                            ent.draw_name()
                    except Exception as e:
                        continue
            pm.end_drawing()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(400, 300)
    widget.show()

    overlay_thread = OverlayThread()
    overlay_thread.start()

    sys.exit(app.exec())
