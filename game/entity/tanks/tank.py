from abc import abstractmethod, ABC

from entity.entity import Entity


class Tank(Entity, ABC):
    """ Abstract Tank class """
    __damage = 1

    def __init__(self, tank_id: int, tank_info: dict, colour: str, player_index: int, image_path: str):
        self.__tank_id = tank_id
        self.__hp: int = tank_info["health"]
        self.__og_hp: int = self.__hp
        self.__cp: int = tank_info["capture_points"]
        self.__spawn_coord: tuple = (tank_info["spawn_position"]["x"],
                                     tank_info["spawn_position"]["y"],
                                     tank_info["spawn_position"]["z"])
        self.__tank_colour: str = colour
        self.__player_index: int = player_index
        self.__destroyed: bool = False
        self._coord: tuple = (tank_info["position"]["x"],
                              tank_info["position"]["y"],
                              tank_info["position"]["z"])

        self.__image_path: str = image_path

        super().__init__(tank_info["vehicle_type"])

    def update_hp(self, hp: int):
        self.__hp = hp

    def update_cp(self, capture_pts: int):
        self.__cp = capture_pts

    def register_hit_return_destroyed(self) -> bool:
        self.__hp -= Tank.__damage  # All tanks do 1 damage
        if self.__hp < 1:
            self.__destroyed = True

        return self.__destroyed

    def respawn(self) -> None:
        self.__destroyed = False
        self.__hp = self.__og_hp

    """     GETTERS     """

    def get_coord(self) -> tuple: return self._coord

    def get_player_index(self) -> int: return self.__player_index

    def get_id(self) -> int: return self.__tank_id

    def get_color(self) -> str: return self.__tank_colour

    def get_hp(self) -> int: return self.__hp

    def get_max_hp(self) -> int: return self.__og_hp

    def is_destroyed(self) -> bool: return self.__destroyed

    def get_cp(self) -> int: return self.__cp

    def get_spawn_coord(self) -> tuple: return self.__spawn_coord

    def get_image_path(self) -> str:
        return self.__image_path

    """     SETTERS     """

    def set_coord(self, new_coord: tuple) -> None:
        self._coord = new_coord

    def set_hp(self, hp: int): self.__hp = hp

    def set_cp(self, capture_pts: int): self.__cp = capture_pts

    """     ABSTRACTS       """

    @abstractmethod
    def shot_moves(self, target: tuple) -> tuple: pass  # sorted coords to where "self" can move to shoot "target"

    @abstractmethod
    def get_speed(self) -> int: pass

    @abstractmethod
    def is_too_far(self, target: tuple) -> bool: pass  # True: too far to shoot, Null: just right, False: too close

    @abstractmethod
    def get_fire_deltas(self) -> tuple: pass

    @abstractmethod
    def coords_in_range(self) -> tuple: pass

    @abstractmethod
    def td_shooting_coord(self, target: tuple) -> tuple: pass

    @abstractmethod
    def fire_corridors(self) -> tuple: pass
