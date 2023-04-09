from abc import ABC

from src.entity.entity import Entity
from src.map.hex import Hex


class Tank(Entity, ABC):
    __damage = 1

    def __init__(self, tank_id: int, tank_info: dict, colour: str):
        self.__tank_id = tank_id
        self.__hp: int = tank_info["health"]
        self.__og_hp: int = self.__hp
        self.__capture_points = tank_info["capture_points"]
        self.__spawn_pos: Hex = Hex([tank_info["position"]["x"],
                                     tank_info["position"]["y"],
                                     tank_info["position"]["z"]])
        self.__position: Hex = self.__spawn_pos
        self.__tank_colour: str = colour

        super().__init__(tank_info["vehicle_type"])

    def update(self, hp: int, capture_pts: int):
        self.__hp = hp
        self.__capture_points = capture_pts

    def reset(self) -> None:
        self.__hp = self.__og_hp

    def reduce_hp(self) -> bool:
        """
        Registers tank hit.
        :return: True if tank is destroyed, False otherwise"""
        self.__hp -= self.__damage
        if self.__hp <= 0:
            self.reset()
            return True
        return False

    def get_spawn_pos(self) -> Hex:
        return self.__spawn_pos

    def get_id(self) -> int:
        return self.__tank_id

    def get_symbol(self) -> str:
        if self._type == 'spg':
            return 's'
        if self._type == 'at_spg':
            return 'v'
        if self._type == 'heavy_tank':
            return 'H'
        if self._type == 'medium_tank':
            return '*'
        if self._type == 'light_tank':
            return 'D'

    def get_colour(self) -> str:
        return self.__tank_colour

    def get_pos(self) -> Hex:
        return self.__position

    def get_coords(self) -> tuple:
        return self.__position.get_coords()

    def set_pos(self, position: Hex) -> None:
        self.__position = position
