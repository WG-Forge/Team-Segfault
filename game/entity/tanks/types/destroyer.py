from abc import ABC

from entity.tanks.tank import Tank
from map.hex import Hex


class TankDestroyer(Tank, ABC):
    __sp: int = 1  # Speed Points
    __dp: int = 2  # Destruction Points
    __fire_deltas: tuple = Hex.make_directions(3)
    __symbol: str = 'v'

    def __init__(self, tank_id: int, tank_info: dict, colour: str, player_index: int):
        super().__init__(tank_id, tank_info, colour, player_index)

    def get_possible_shots(self) -> tuple:
        x, y, z = self._coord
        return tuple([(dx + x, dy + y, dz + z) for (dx, dy, dz) in TankDestroyer.__fire_deltas])

    def get_speed(self) -> int:
        return self.__sp

    def get_symbol(self) -> str:
        return TankDestroyer.__symbol

    def get_tank_type_shape(self, x: int, y: int, radius_x: int, radius_y: int) -> ([], bool):
        return [(x, y - 0.4325), (x - 0.5, y + 0.4325), (x + 0.5, y + 0.4325)], True
