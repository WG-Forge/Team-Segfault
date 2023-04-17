from enum import Enum
from threading import Semaphore, Event

from player.bot_player import BotPlayer
from player.human_player import HumanPlayer
from player.player import Player


class PlayerTypes(Enum):
    Human = 1
    Bot = 2


class PlayerMaker:
    __CLASS_MAPPING = {
        PlayerTypes.Human: HumanPlayer,
        PlayerTypes.Bot: BotPlayer
    }

    @staticmethod
    def create_player(player_type: PlayerTypes,
                      turn_played_sem: Semaphore,
                      current_player_idx: list[1],
                      active: Event,
                      player_index: int,
                      name: str,
                      password: str = None,
                      is_observer: bool = None) -> Player:
        player_class = PlayerMaker.__CLASS_MAPPING[player_type]
        return player_class(name, password, is_observer, turn_played_sem, current_player_idx, player_index, active)
