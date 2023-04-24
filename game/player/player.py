from abc import abstractmethod
from dataclasses import dataclass
from threading import Thread, Semaphore, Event
from typing import Union

from client.game_client import GameClient
from entity.tanks.tank import Tank
from map.map import Map


@dataclass
class Player(Thread):
    __type_order = ('spg', 'light_tank', 'heavy_tank', 'medium_tank', 'at_spg')
    __possible_colours = ((224, 206, 70), (70, 191, 224), (201, 26, 40))  # yellow, blue, red

    def __init__(self,
                 turn_played_sem: Semaphore, current_player: list[1], player_index: int, over: Event,
                 name: str = None, password: str = None, is_observer: bool = None):
        super().__init__()

        self.idx: int = -1
        self.name = name
        self.password = password
        self.is_observer: bool = is_observer

        self.next_turn_sem = Semaphore(0)
        self._current_player = current_player
        self.__turn_played_sem = turn_played_sem
        self.__over = over

        self._game_client: GameClient | None = None
        self._map: Map | None = None

        self._damage_points = 0
        self._capture_points = 0
        self._tanks: list[Tank] = []
        self._tank_map: dict[int, Tank] = {}
        self._player_index = player_index
        self.__player_colour = Player.__possible_colours[player_index]
        self.__has_shot = []  # Holds a list of enemies this player has shot last turn

        self._game_actions: Union[dict, None] = None

        self._turn_actions: Union[dict, None] = None

    def __hash__(self):
        return super.__hash__(self)

    def __str__(self):
        out = str.format(f'Player {self.idx}: {self.name}')
        if self.is_observer:
            out += ', observer'

        return out

    def add_to_game(self, player_info: dict, game_client: GameClient):
        self.name: str = player_info["name"]
        self.idx: int = player_info["idx"]
        self.is_observer: bool = player_info["is_observer"]
        self._damage_points: int = 0
        self._capture_points: int = 0
        self._game_client: GameClient = game_client

    def add_tank(self, new_tank: Tank) -> None:
        # Adds the tank in order of who gets priority movement
        new_tank_priority = Player.__type_order.index(new_tank.get_type())
        for i, old_tank in enumerate(self._tanks):
            old_tank_priority = Player.__type_order.index(old_tank.get_type())
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

    def get_color(self) -> str:
        return self.__player_colour

    def get_index(self):
        return self._player_index

    def get_tanks(self):
        return self._tanks

    def has_shot(self, player_index: int) -> bool:
        return player_index in self.__has_shot

    def get_capture_points(self) -> int:
        return sum(tank.get_cp() for tank in self._tanks)

    def get_damage_points(self) -> int:
        return self._damage_points

    def set_turn_actions(self, actions: dict) -> None:
        self._turn_actions = actions

    def register_shot(self, enemy_index: int) -> None:
        self.__has_shot.append(enemy_index)

    def register_turn(self) -> None:  # Call this for every player at the beginning of every turn
        self.__has_shot = []

    def register_destroyed_vehicle(self, tank: Tank) -> None:
        self._damage_points += tank.get_max_hp()

    @abstractmethod
    def _make_turn_plays(self) -> None:
        pass

    @abstractmethod
    def _finalize(self):
        pass
