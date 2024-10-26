import logging
import pyMeow as pm

from aimbot import aim_at_enemy
from config import process, base_address
from entity import Entity
from world import World
from pointers import ENTITY_LIST, PLAYER_COUNT, VIEW_MATRIX, LOCAL_PLAYER


logger = logging.getLogger(__name__)


player = Entity(process=process, address=pm.r_int(process, base_address + LOCAL_PLAYER))
world = World()


def run() -> None:
    pm.overlay_init(target="AssaultCube", fps=60, trackTarget=True)
    while pm.overlay_loop():
        pm.begin_drawing()
        pm.draw_fps(10, 10)
        try:
            player = Entity(
                process=process,
                address=pm.r_int(process, base_address + LOCAL_PLAYER),
            )
        except Exception as e:
            logger.exception(e)
            continue
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
                        ent.draw_box()
                        ent.draw_name()
                        ent.draw_health()
                    if pm.mouse_pressed("right") and ent.is_alive():
                        aim_at_enemy(player, ent)
                except Exception as e:
                    logger.exception(e)
                    continue
        pm.end_drawing()


if __name__ == "__main__":
    run()
