from abc import ABC
from threading import Semaphore

from src.player.player import Player


class HumanPlayer(Player, ABC):
    def __init__(self, name: str, password: str, is_observer: bool,
                 turn_played_sem: Semaphore, current_player: list[1]):
        super().__init__(name, password, is_observer, turn_played_sem, current_player)

    def _play_move(self) -> None:
        pass
