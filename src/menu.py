import pyMeow as pm


class Menu:
    def __init__(self) -> None:
        self.show = True

    def draw(self) -> None:
        if not self.show:
            return

        pm.gui_window_box(
            posX=0, posY=0, width=400, height=210, title="AssaultCube Cheats"
        )
        pm.gui_load_style("src/style_dark.rgs")
