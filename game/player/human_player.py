from abc import ABC
from threading import Semaphore

from game.player.player import Player


class HumanPlayer(Player, ABC):
    def __init__(self, name: str, password: str, is_observer: bool,
                 turn_played_sem: Semaphore, current_player: list[1], player_index: int):
        super().__init__(name, password, is_observer, turn_played_sem, current_player, player_index)

    def _make_turn_plays(self) -> None:
        pass
