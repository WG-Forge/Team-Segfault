from abc import abstractmethod

from game_map.map import Map
from src.entities.tanks.tank import Tank


class LocalPlayer:
    __type_order = ('spg', 'light_tank', 'heavy_tank', 'medium_tank', 'at_spg')

    def __init__(self, player_index: int):

        self.idx: int = -1
        self._map: Map | None = None

        self._damage_points = 0
        self._tanks: list[Tank] = []
        self._tank_map: dict[int, Tank] = {}
        self._player_index: int = player_index
        self.__player_colour: tuple | None = None
        self.__has_shot: list[int] = []  # Holds a list of enemies this player has shot last turn
        self.__is_observer: bool = False

        self._game_actions: dict | None = None
        self._turn_actions: dict | None = None

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
    def color(self) -> tuple:
        return self.__player_colour

    @property
    def tanks(self) -> list[Tank]:
        return self._tanks

    @property
    def damage_points(self) -> int:
        return self._damage_points

    @property
    def turn_actions(self) -> dict | None:
        return self._turn_actions

    @turn_actions.setter
    def turn_actions(self, actions: dict) -> None:
        self._turn_actions = actions

    @property
    def index(self) -> int | None:
        return self._player_index

    @index.setter
    def index(self, player_index: int) -> None:
        self._player_index = player_index

    @property
    def is_observer(self) -> bool:
        return self.__is_observer

    """     MISC        """

    def register_shot(self, enemy_index: int) -> None:
        self.__has_shot.append(enemy_index)

    def register_turn(self) -> None:  # Call this for every player at the beginning of every turn
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
