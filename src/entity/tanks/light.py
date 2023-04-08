from abc import ABC

from entity.tanks.hex_deltas import HexDeltas
from entity.tanks.tank import Tank


class LightTank(Tank, ABC):
    __sp: int = 3  # Speed Points
    __dp: int = 1  # Destruction Points
    __fire_deltas: tuple = HexDeltas.rings[1]  # Fires only in ring2
    __possible_shot_num: int = len(__fire_deltas)

    def __init__(self, tank_id: int, tank_info: dict):
        super().__init__(tank_id, tank_info)

    def get_possible_shots(self, position: tuple) -> tuple:
        dx, dy, dz = position
        return tuple([(dx+x, dy+y, dz+z) for (x, y, z) in LightTank.__fire_deltas])


