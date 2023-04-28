from abc import abstractmethod
from dataclasses import dataclass
from threading import Event
from typing import Union, Dict

from client.server_enum import Action
from constants import PLAYER1_COLOR, PLAYER2_COLOR, PLAYER3_COLOR
from constants import PLAYER_COLORS
from entity.entity_enum import Entities
from entity.tanks.tank import Tank
from map.map import Map


@dataclass
class Player:
    __type_order = (
        Entities.ARTILLERY, Entities.LIGHT_TANK, Entities.HEAVY_TANK, Entities.MEDIUM_TANK, Entities.TANK_DESTROYER)
    __possible_colours = (PLAYER1_COLOR, PLAYER2_COLOR, PLAYER3_COLOR)

    def __init__(self, player_index: int, over: Event, name: str = None, password: str = None,
                 is_observer: bool = None):

        self.__idx: int = -1
        self.__name = name
        self.__password = password
        self.__is_observer: bool = is_observer

        self.__over: Event = over

        self._map: Map | None = None

        self._damage_points: int = 0
        self._capture_points: int = 0
        self._tanks: list[Tank] = []
        self._tank_map: Dict[int, Tank] = {}
        # todo remove color information from player class
        self.__player_color: tuple[int, int, int] | str = PLAYER_COLORS[player_index]
        self.__has_shot = []  # Holds a list of enemies this player has shot last turn

        self._game_actions: Union[Dict, None] = None

        self._turn_actions: list[tuple[Action, Dict]] | None = None

    def __str__(self):
        out = str.format(f'Player {self.__idx}: {self.__name}')
        if self.__is_observer:
            out += ', observer'

        return out

    def add_to_game(self, player_info: Dict):
        self.__name: str = player_info["name"]
        self.__idx: int = player_info["idx"]
        self.__is_observer: bool = player_info["is_observer"]
        self._damage_points: int = 0
        self._capture_points: int = 0

    def add_tank(self, new_tank: Tank) -> None:
        # Adds the tank in order of who gets priority movement
        new_tank_priority = Player.__type_order.index(new_tank.type)
        for i, old_tank in enumerate(self._tanks):
            old_tank_priority = Player.__type_order.index(old_tank.type)
            if new_tank_priority <= old_tank_priority:
                self._tanks.insert(i, new_tank)
                return
        self._tanks.append(new_tank)

    def add_map(self, game_map: Map):
        self._map = game_map

    @property
    def idx(self) -> int:
        return self.__idx

    @property
    def name(self) -> str:
        return self.__name

    @property
    def password(self) -> str:
        return self.__password

    @property
    def is_observer(self) -> bool:
        return self.__is_observer

    @property
    def color(self) -> str:
        return self.__player_color

    @property
    def tanks(self) -> list[Tank]:
        return self._tanks

    def has_shot(self, player_index: int) -> bool:
        return player_index in self.__has_shot

    @property
    def capture_points(self) -> int:
        return sum(tank.cp for tank in self._tanks)

    @property
    def damage_points(self) -> int:
        return self._damage_points

    @property
    def turn_actions(self) -> list[tuple[Action, Dict]]:
        return self._turn_actions

    def register_shot(self, enemy_index: int) -> None:
        self.__has_shot.append(enemy_index)

    def register_turn(self) -> None:  # Call this for every player at the beginning of every turn

        self.__has_shot = []

    def register_destroyed_vehicle(self, tank: Tank) -> None:
        self._damage_points += tank.max_hp

    @abstractmethod
    def make_turn_plays(self) -> None:
        pass
