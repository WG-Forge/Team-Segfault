from abc import ABC

from entity.tanks.tank import Tank
from map.hex import Hex


class Artillery(Tank, ABC):
    __sp: int = 1  # Speed Points
    __dp: int = 1  # Destruction Points
    __fire_deltas: tuple = Hex.rings[2]  # Fires only in ring3
    __possible_shot_num: int = len(__fire_deltas)
    __symbol: str = 's'

    def __init__(self, tank_id: int, tank_info: dict, colour: str, player_index: int):
        super().__init__(tank_id, tank_info, colour, player_index)

    def get_possible_shots(self) -> tuple:
        x, y, z = self._coord
        return tuple([(dx + x, dy + y, dz + z) for (dx, dy, dz) in Artillery.__fire_deltas])

    def get_speed(self) -> int:
        return self.__sp

    def get_symbol(self) -> str:
        return Artillery.__symbol

    def get_tank_type_shape(self, x: int, y: int, radius_x: int, radius_y: int) -> ([], bool):
        edge_len = 0.4
        return [(x + i, y + j) for i, j in
                [(edge_len, edge_len), (-edge_len, edge_len), (-edge_len, -edge_len), (edge_len, -edge_len)]], True
