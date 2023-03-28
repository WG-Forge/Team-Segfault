import json

from src.entity.tank import Tank
from src.game import Game


class Player:
    def __init__(self, player_info: str):
        player_info = json.loads(player_info)
        self.__id: int = player_info["idx"]
        self.__name: str = player_info["name"]
        self.is_observer: bool = player_info["is_observer"]
        self.__damage_points: int = 0
        self.__capture_points: int = 0
        self.__tanks: list[Tank]
        self.__game: Game

    def play_move(self) -> str:
        pass
