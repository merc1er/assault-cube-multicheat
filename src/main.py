import sys

from PySide6 import QtCore, QtWidgets, QtGui
import pyMeow as pm

from config import process, base_address
from entity import Entity
from world import World


player = Entity(process, base_address)
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
            pm.end_drawing()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(400, 300)
    widget.show()

    overlay_thread = OverlayThread()
    overlay_thread.start()

    sys.exit(app.exec())
