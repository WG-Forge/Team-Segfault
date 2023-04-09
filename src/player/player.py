from abc import abstractmethod
from dataclasses import dataclass
from threading import Thread, Semaphore

from src.client.game_client import GameClient
from src.entity.tanks.tank import Tank
from src.map.game_map import GameMap


@dataclass
class Player(Thread):
    __type_order = ('spg', 'light_tank', 'heavy_tank', 'medium_tank', 'at_spg')
    __possible_colours = ('blue', 'black', 'green')

    def __init__(self, name: str, password: str, is_observer: bool,
                 turn_played_sem: Semaphore, current_player: list[1], player_index: int):
        super().__init__(daemon=True)
        self.idx: int = -1
        self.name = name
        self.password = password
        self.is_observer: bool = is_observer
        self.next_turn_sem = Semaphore(0)
        self._damage_points = 0
        self._capture_points = 0
        self._tanks: list[Tank] = []
        self._game_map = None
        self._game_client = None
        self.__turn_played_sem = turn_played_sem
        self.__current_player = current_player
        self.__player_colour = Player.__possible_colours[player_index]

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        out = str.format(f'Player {self.idx}: {self.name}')
        if self.is_observer:
            out += ', observer'

        return out

    def add_to_game(self, player_info: dict, game_client: GameClient):
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

    def add_map(self, game_map: GameMap):
        self._game_map = game_map

    def run(self) -> None:
        while True:
            # wait for condition
            self.next_turn_sem.acquire()

            # play your move if you are the current player
            if self.__current_player[0] == self.idx:
                self._play_move()

            # force next turn
            self._game_client.force_turn()

            # notify condition
            self.__turn_played_sem.release()

    @abstractmethod
    def _play_move(self) -> None:
        pass

    def get_colour(self) -> str:
        return self.__player_colour
