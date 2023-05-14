from abc import abstractmethod

from src.entities.tanks.tank import Tank
from src.game_map.map import Map


class LocalPlayer:
    """ Abstract base player class """
    __type_order = ('spg', 'light_tank', 'heavy_tank', 'medium_tank', 'at_spg')

    def __init__(self, player_idx: int):
        super().__init__()

        self.idx: int = player_idx
        self._map: Map | None = None

        self._damage_points: int = 0
        self._capture_points: int = 0

        self._tanks: list[Tank] = []
        self.__has_shot: list[int] = []  # Holds a list of enemies this player has shot last turn

        self.is_observer = False
        self.color = 'none'

    def add_tank(self, new_tank: Tank) -> None:
        # Adds the tank in order of who gets priority movement
        new_tank_priority = LocalPlayer.__type_order.index(new_tank.type)
        for i, old_tank in enumerate(self._tanks):
            old_tank_priority = LocalPlayer.__type_order.index(old_tank.type)
            if new_tank_priority <= old_tank_priority:
                self._tanks.insert(i, new_tank)
                return
        self._tanks.append(new_tank)

    def add_map(self, game_map: Map) -> None:
        self._map = game_map

    def run(self) -> None:
        self._make_turn_plays()

    """     GETTERS AND SETTERS    """

    @property
    def tanks(self) -> list[Tank]:
        return self._tanks

    @property
    def capture_points(self) -> int:
        return sum([tank.capture_points for tank in self._tanks])

    @capture_points.setter
    def capture_points(self, capture_points: int) -> None:
        self._capture_points = capture_points

    @property
    def damage_points(self) -> int:
        return self._damage_points

    @damage_points.setter
    def damage_points(self, damage_points: int) -> None:
        self._damage_points = damage_points

    """     MISC        """

    def register_shot(self, enemy_index: int) -> None:
        self.__has_shot.append(enemy_index)

    def register_round(self) -> None:
        self._damage_points = 0
        self._tanks = []

    def register_turn(self) -> None:
        self.__has_shot = []

    def register_destroyed_vehicle(self, tank: Tank) -> None:
        self._damage_points += tank.max_health_points

    def has_shot(self, player_index: int) -> bool:
        return player_index in self.__has_shot

    """     ABSTRACTS       """

    @abstractmethod
    def _make_turn_plays(self) -> None:
        pass

    """     ML      """

    def has_capped(self) -> bool:
        capture_points = sum([tank.capture_points for tank in self._tanks])
        # print('capture_points', capture_points)
        if capture_points > 4:
            return True
        return False
