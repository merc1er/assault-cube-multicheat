import sys
import logging
from PySide6 import QtCore, QtWidgets, QtGui
import pyMeow as pm

from aimbot import aim_at_enemy
from config import check_process
from entity import Entity
from world import World
from pointers import ENTITY_LIST, PLAYER_COUNT, VIEW_MATRIX, LOCAL_PLAYER


logger = logging.getLogger(__name__)
player = None
world = None
process = None
base_address = None


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Set up the window.
        self.setWindowTitle("p1nkrat's AssaultCube trainer")
        self.setWindowIcon(QtGui.QIcon("logo.png"))
        self.layout = QtWidgets.QVBoxLayout(self)

        # Status message.
        self.status_label = QtWidgets.QLabel(
            "AssaultCube not found. Make sure it is running.",
            alignment=QtCore.Qt.AlignCenter,
        )
        self.layout.addWidget(self.status_label)

        # Increase health.
        self.increase_health_button = QtWidgets.QPushButton("❤️‍🩹 Increase health")
        self.increase_health_button.clicked.connect(lambda: player.set_health())
        self.layout.addWidget(self.increase_health_button)

        # Increase ammo.
        self.increase_ammo_button = QtWidgets.QPushButton("⬆️ Increase ammo")
        self.increase_ammo_button.clicked.connect(lambda: player.set_all_ammo())
        self.layout.addWidget(self.increase_ammo_button)

        # Enable jump hack.
        self.jump_hack_button = QtWidgets.QPushButton("🦘 Enable jump hack")
        self.jump_hack_button.clicked.connect(self.toggle_jump_hack)
        self.layout.addWidget(self.jump_hack_button)

        # Hide the buttons initially.
        self.increase_health_button.hide()
        self.increase_ammo_button.hide()
        self.jump_hack_button.hide()

        # Timer to check for the process.
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.check_game_status)
        self.timer.start(1000)  # Check every second

    def check_game_status(self) -> None:
        global process, base_address, player
        process_info = check_process()
        if process_info:
            self.timer.stop()  # Stop the timer once the process is found
            process, base_address = process_info
            player = Entity(
                process=process, address=pm.r_int(process, base_address + LOCAL_PLAYER)
            )
            self.world = World(process, base_address)

            # Update UI
            self.status_label.hide()
            self.increase_health_button.show()
            self.increase_ammo_button.show()
            self.jump_hack_button.show()

            # Start the overlay thread.
            overlay_thread = OverlayThread()
            overlay_thread.start()

    def toggle_jump_hack(self) -> None:
        if self.jump_hack_button.text() == "🦘 Enable jump hack":
            self.jump_hack_button.setText("🦘 Disable jump hack")
            self.world.enable_jump_hack()
        else:
            self.jump_hack_button.setText("🦘 Enable jump hack")
            self.world.disable_jump_hack()


class OverlayThread(QtCore.QThread):
    """
    Custom thread to run the while loop in the background.
    """

    def run(self):
        pm.overlay_init(target="AssaultCube", fps=60, trackTarget=True)
        while pm.overlay_loop():
            pm.begin_drawing()
            pm.draw_fps(10, 10)
            if not player:
                continue
            try:
                player_count = pm.r_int(process, base_address + PLAYER_COUNT)
                if player_count > 1:
                    ent_buffer = pm.r_ints(
                        process,
                        pm.r_int(process, base_address + ENTITY_LIST),
                        player_count,
                    )[1:]
                    v_matrix = pm.r_floats(process, base_address + VIEW_MATRIX, 16)
                    for address in ent_buffer:
                        try:
                            ent = Entity(process, address)
                            if ent.world_to_screen(v_matrix):
                                ent.draw_box()
                                ent.draw_name()
                                ent.draw_health()
                            if pm.mouse_pressed("right") and ent.is_alive():
                                aim_at_enemy(player, ent)
                        except Exception as e:
                            logger.exception(e)
                            continue
            except Exception as e:
                logger.exception(e)
            pm.end_drawing()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(300, 150)
    widget.show()

    sys.exit(app.exec())
