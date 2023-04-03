from abc import abstractmethod
from dataclasses import dataclass
from threading import Thread, Semaphore

from src.client.game_client import GameClient
from src.entity.tank import Tank
from src.map.game_map import GameMap


@dataclass
class Player(Thread):
    def __init__(self, name: str, password: str, is_observer: bool,
                 turn_played_sem: Semaphore, current_player: list[1]):
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

    def add_tank(self, tank: Tank):
        self._tanks.append(tank)

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
