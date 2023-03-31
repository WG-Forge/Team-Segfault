from abc import ABC

from src.player.player import Player


class BotPlayer(Player, ABC):
    def __init__(self, name: str, password: str = None, is_observer: bool = None):
        super().__init__(name, password, is_observer)

    def play_move(self) -> str:
        pass
