from abc import ABC

from map.hex import Hex
from entity.tanks.tank import Tank


class TankDestroyer(Tank, ABC):
    __sp: int = 1  # Speed Points
    __dp: int = 2  # Destruction Points
    # Special case of fire_deltas where all coords with a 0 are eliminated to create TD fire pattern
    __fire_deltas: tuple = tuple(filter(lambda t: 0 not in t, tuple(Hex.rings[:2])))
    __possible_shot_num: int = len(__fire_deltas)

    def __init__(self, tank_id: int, tank_info: dict, colour: str):
        super().__init__(tank_id, tank_info, colour)

    def get_possible_shots(self, position: tuple) -> tuple:
        x, y, z = position
        return tuple([(dx+x, dy+y, dz+z) for (dx, dy, dz) in TankDestroyer.__fire_deltas])

    def get_speed(self) -> int:
        return self.__sp
