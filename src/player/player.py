from abc import abstractmethod
from dataclasses import dataclass

from src.entity.tank import Tank
from src.map.game_map import GameMap


@dataclass
class Player:
    def __init__(self, name: str, password: str = None, is_observer: bool = None):
        self.id = None
        self.is_observer = is_observer
        self.name = name
        self.password = password
        self._damage_points = 0
        self._capture_points = 0
        self._tanks: list[Tank] = []
        self._game_map: GameMap = None

    def add_to_game(self, player_info: dict):
        self.id: int = player_info["idx"]
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
