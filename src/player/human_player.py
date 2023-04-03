from abc import ABC

from src.player.player import Player


class HumanPlayer(Player, ABC):
    def __init__(self, name: str, password: str = None, is_observer: bool = False):
        super().__init__(name, password, is_observer)

    def play_move(self) -> (dict, dict):
        return None, None
