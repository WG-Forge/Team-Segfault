from abc import abstractmethod, ABC
from typing import Tuple

from entities.entity import Entity, Entities


class Tank(Entity, ABC):
    """ Abstract Tank class """
    __damage = 1

    def __init__(self, tank_id: int, tank_info: dict, color: Tuple[int, int, int] | str, player_index: int,
                 image_path: str, catapult_coords: Tuple):
        self.__tank_id = tank_id
        self.__hp: int = tank_info["health"]
        self.__og_hp: int = self.__hp
        self.__cp: int = tank_info["capture_points"]
        self.__spawn_coord: tuple = (tank_info["spawn_position"]["x"],
                                     tank_info["spawn_position"]["y"],
                                     tank_info["spawn_position"]["z"])
        self.__tank_color = color
        self.__player_index: int = player_index
        self.__destroyed: bool = False
        self._coord: tuple = (tank_info["position"]["x"],
                              tank_info["position"]["y"],
                              tank_info["position"]["z"])

        self._catapult_coords: Tuple = catapult_coords
        self.__image_path: str = image_path

        super().__init__(Entities(tank_info["vehicle_type"]))

    def register_hit_return_destroyed(self) -> bool:
        self.__hp -= Tank.__damage  # All tanks do 1 damage
        if self.__hp < 1:
            self.__destroyed = True

        return self.__destroyed

    def respawn(self) -> None:
        self.__destroyed = False
        self.__hp = self.__og_hp

    """     GETTERS AND SETTERS     """

    @property
    def coord(self) -> tuple: return self._coord

    @coord.setter
    def coord(self, new_coord: tuple) -> None:
        self._coord = new_coord

    @property
    def player_index(self) -> int: return self.__player_index

    @property
    def tank_id(self) -> int: return self.__tank_id

    @property
    def color(self) -> str | Tuple[int, int, int]: return self.__tank_color

    @property
    def hp(self) -> int: return self.__hp

    @hp.setter
    def hp(self, hp: int): self.__hp = hp

    @property
    def max_hp(self) -> int: return self.__og_hp

    @property
    def is_destroyed(self) -> bool: return self.__destroyed

    @property
    def cp(self) -> int: return self.__cp

    @cp.setter
    def cp(self, capture_pts: int): self.__cp = capture_pts

    @property
    def spawn_coord(self) -> tuple: return self.__spawn_coord

    @property
    def image_path(self) -> str:
        return self.__image_path

    """     ABSTRACTS       """

    @abstractmethod
    def shot_moves(self, target: tuple) -> tuple: pass  # sorted coords to where "self" can move to shoot "target"

    @property
    @abstractmethod
    def speed(self) -> int: pass

    @abstractmethod
    def coords_in_range(self, is_on_catapult: bool) -> Tuple: pass

    @abstractmethod
    def td_shooting_coord(self, target: tuple) -> tuple: pass

    @abstractmethod
    def fire_corridors(self) -> tuple: pass
