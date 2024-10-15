import pyMeow as pm
from PySide6 import QtCore, QtWidgets, QtGui

from entity import Entity


process_name = "ac_client.exe"

try:
    process = pm.open_process(process_name)
    base_address = pm.get_module(process, process_name)["base"]
    print(f"Process found at 0x{base_address:x}.")
except Exception:
    print(f"Process {process_name} not found. Make sure Assault Cube is running.")
    exit()


player = Entity(process, base_address)


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


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(400, 300)
    widget.show()

    exit(app.exec())
