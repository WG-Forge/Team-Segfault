from abc import abstractmethod
from dataclasses import dataclass

from src.entity.tank import Tank


@dataclass
class Player:
    def __init__(self, name: str, password: str = None, is_observer: bool = None):
        self.id = None
        self.is_observer = is_observer
        self.name = name
        self.password = password
        self.__damage_points = 0
        self.__capture_points = 0
        self.__tanks: list[Tank]

    def add_to_game(self, player_info: dict):
        self.id: int = player_info["idx"]
        self.is_observer: bool = player_info["is_observer"]
        self.__damage_points: int = 0
        self.__capture_points: int = 0

    @abstractmethod
    def play_move(self) -> str:
        pass
