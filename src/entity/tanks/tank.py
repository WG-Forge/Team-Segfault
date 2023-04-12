from abc import ABC, abstractmethod

from src.entity.entity import Entity


class Tank(Entity, ABC):
    __damage = 1

    def __init__(self, tank_id: int, tank_info: dict, colour: str, player_index: int):
        self.__tank_id = tank_id
        self.__hp: int = tank_info["health"]
        self.__og_hp: int = self.__hp
        self.__capture_points = tank_info["capture_points"]
        self.__spawn_coord: tuple = (tank_info["position"]["x"], tank_info["position"]["y"], tank_info["position"]["z"])
        self._coord: tuple = self.__spawn_coord
        self.__tank_colour: str = colour
        self.__player_index: int = player_index

        super().__init__(tank_info["vehicle_type"])

    def update(self, hp: int, capture_pts: int):
        self.__hp = hp
        self.__capture_points = capture_pts

    def reset(self) -> None:
        self.__hp = self.__og_hp
        self.__coord = self.__spawn_coord

    def reduce_hp(self) -> bool:
        """
        Registers tank hit.
        :return: True if tank is destroyed, False otherwise"""
        self.__hp -= self.__damage
        if self.__hp <= 0:
            self.reset()
            return True
        return False

    def get_spawn_coord(self) -> tuple:
        return self.__spawn_coord

    def get_id(self) -> int:
        return self.__tank_id

    def get_player_index(self) -> int:
        return self.__player_index

    def get_color(self) -> str:
        return self.__tank_colour

    def get_coord(self) -> tuple:
        return self._coord

    def set_coord(self, new_coord: tuple) -> None:
        self._coord = new_coord

    def in_range(self, target: tuple) -> bool:
        return target in self.get_possible_shots()

    @abstractmethod
    def get_symbol(self) -> str:
        pass

    @abstractmethod
    def get_speed(self) -> int:
        pass

    @abstractmethod
    def get_possible_shots(self):
        pass

    def get_hp(self) -> int:
        return self.__hp
