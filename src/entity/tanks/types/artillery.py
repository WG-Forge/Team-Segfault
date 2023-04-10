from abc import ABC

from entity.tanks.tank import Tank
from map.hex import Hex


class Artillery(Tank, ABC):
    __sp: int = 1  # Speed Points
    __dp: int = 1  # Destruction Points
    __fire_deltas: tuple = Hex.rings[2]  # Fires only in ring3
    __possible_shot_num: int = len(__fire_deltas)

    def __init__(self, tank_id: int, tank_info: dict, colour: str):
        super().__init__(tank_id, tank_info, colour)

    def get_possible_shots(self, position: tuple) -> tuple:
        x, y, z = position
        return tuple([(dx+x, dy+y, dz+z) for (dx, dy, dz) in Artillery.__fire_deltas])

    def get_speed(self) -> int:
        return self.__sp






