import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QPen


class CrosshairOverlay(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window to be transparent and always on top
        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.X11BypassWindowManagerHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlag(Qt.Tool)

        # Set the size to full screen
        self.showFullScreen()

        # Create a timer to keep the window on top every 100ms
        self.timer = QTimer()
        self.timer.timeout.connect(self.raise_window)
        self.timer.start(100)

    def raise_window(self):
        self.raise_()

    def paintEvent(self, event):
        # Draw the crosshair at the center of the screen
        painter = QPainter(self)
        pen = QPen(Qt.red, 3)  # You can customize the color and thickness here
        painter.setPen(pen)

        screen_width = self.width()
        screen_height = self.height()

        # Draw a crosshair at the center
        center_x = screen_width // 2
        center_y = screen_height // 2

        painter.drawLine(
            center_x - 20, center_y, center_x + 20, center_y
        )  # Horizontal line
        painter.drawLine(
            center_x, center_y - 20, center_x, center_y + 20
        )  # Vertical line


def main():
    app = QApplication(sys.argv)
    overlay = CrosshairOverlay()
    overlay.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
