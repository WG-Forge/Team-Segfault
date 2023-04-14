from abc import ABC

from map.hex import Hex
from ..tank import Tank


class HeavyTank(Tank, ABC):
    __sp: int = 1  # Speed Points
    __dp: int = 3  # Destruction Points
    __fire_deltas: tuple = Hex.rings[0] + Hex.rings[1]  # Fires in rings 1&2
    __possible_shot_num: int = len(__fire_deltas)
    __symbol: str = 'H'

    def __init__(self, tank_id: int, tank_info: dict, colour: str, player_index: int):
        super().__init__(tank_id, tank_info, colour, player_index)

    def get_possible_shots(self) -> tuple:
        x, y, z = self._coord
        return tuple([(dx + x, dy + y, dz + z) for (dx, dy, dz) in HeavyTank.__fire_deltas])

    def get_speed(self) -> int:
        return self.__sp

    def get_symbol(self) -> str:
        return HeavyTank.__symbol
