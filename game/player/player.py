from abc import abstractmethod
from dataclasses import dataclass
from threading import Thread, Semaphore, Event
from typing import Union, Dict

from client.game_client import GameClient
from constants import PLAYER1_COLOR, PLAYER2_COLOR, PLAYER3_COLOR
from entity.entity_enum import Entities
from entity.tanks.tank import Tank
from map.map import Map


@dataclass
class Player(Thread):
    __type_order = (
        Entities.ARTILLERY, Entities.LIGHT_TANK, Entities.HEAVY_TANK, Entities.MEDIUM_TANK, Entities.TANK_DESTROYER)
    __possible_colours = (PLAYER1_COLOR, PLAYER2_COLOR, PLAYER3_COLOR)

    def __init__(self,
                 turn_played_sem: Semaphore, current_player: list[1], player_index: int, over: Event,
                 name: str = None, password: str = None, is_observer: bool = None):
        super().__init__()

        self.idx: int = -1
        self.name = name
        self.password = password
        self.is_observer: bool = is_observer

        self.next_turn_sem = Semaphore(0)
        self._current_player: list[1] = current_player
        self.__turn_played_sem: Semaphore = turn_played_sem
        self.__over: Event = over

        self._game_client: GameClient | None = None
        self._map: Map | None = None

        self._damage_points: int = 0
        self._capture_points: int = 0
        self._tanks: list[Tank] = []
        self._tank_map: Dict[int, Tank] = {}
        self._player_index: int = player_index
        self.__player_colour: tuple[int, int, int] | str = Player.__possible_colours[player_index]
        self.__has_shot = []  # Holds a list of enemies this player has shot last turn

        self._game_actions: Union[Dict, None] = None

        self._turn_actions: Union[Dict, None] = None

    def __hash__(self):
        return super.__hash__(self)

    def __str__(self):
        out = str.format(f'Player {self.idx}: {self.name}')
        if self.is_observer:
            out += ', observer'

        return out

    def add_to_game(self, player_info: Dict, game_client: GameClient):
        self.name: str = player_info["name"]
        self.idx: int = player_info["idx"]
        self.is_observer: bool = player_info["is_observer"]
        self._damage_points: int = 0
        self._capture_points: int = 0
        self._game_client: GameClient = game_client

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

    def run(self) -> None:
        while not self.__over.is_set():
            # wait for condition
            self.next_turn_sem.acquire()

            try:
                # check if the game ended
                if self.__over.is_set():
                    break

                self._make_turn_plays()

            except ConnectionError or TimeoutError as err:
                print(err)
            finally:
                # notify condition
                self.__turn_played_sem.release()

        # finalization
        self._finalize()

    @property
    def color(self) -> str:
        return self.__player_colour

    @property
    def index(self):
        return self._player_index

    @property
    def tanks(self):
        return self._tanks

    def has_shot(self, player_index: int) -> bool:
        return player_index in self.__has_shot

    @property
    def capture_points(self) -> int:
        return sum(tank.cp for tank in self._tanks)

    @property
    def damage_points(self) -> int:
        return self._damage_points

    def set_turn_actions(self, actions: Dict) -> None:
        self._turn_actions = actions

    def register_shot(self, enemy_index: int) -> None:
        self.__has_shot.append(enemy_index)

    def register_turn(self) -> None:  # Call this for every player at the beginning of every turn
        self.__has_shot = []

    def register_destroyed_vehicle(self, tank: Tank) -> None:
        self._damage_points += tank.max_hp

    @abstractmethod
    def _make_turn_plays(self) -> None:
        pass

    @abstractmethod
    def _finalize(self):
        pass
