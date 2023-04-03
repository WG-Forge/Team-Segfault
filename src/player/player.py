from abc import abstractmethod
from dataclasses import dataclass

from src.entity.tank import Tank
from src.map.game_map import GameMap


@dataclass
class Player:
    def __init__(self, name: str, password: str = None, is_observer: bool = None):
        self.idx: int = -1
        self.name = name
        self.password = password
        self.is_observer = is_observer
        self._damage_points = 0
        self._capture_points = 0
        self._tanks: list[Tank] = []
        self._game_map = None

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        out = str.format(f'Player {self.idx}: {self.name}')
        if self.is_observer:
            out += ', observer'

        return out

    def add_to_game(self, player_info: dict):
        self.idx: int = player_info["idx"]
        self.is_observer: bool = player_info["is_observer"]
        self._damage_points: int = 0
        self._capture_points: int = 0

    @abstractmethod
    def play_move(self) -> (dict, dict):
        pass

    def add_tank(self, tank: Tank):
        self._tanks.append(tank)

    def add_map(self, game_map: GameMap):
        self._game_map = game_map
