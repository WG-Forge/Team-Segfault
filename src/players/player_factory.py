from enum import Enum
from threading import Semaphore, Event

from src.players.player import Player
from src.players.types.bot_player import BotPlayer
from src.players.types.observer import Observer
from src.players.types.remote_player import RemotePlayer


class PlayerTypes(Enum):
    Remote = 1
    Bot = 2
    Observer = 3


class PlayerFactory:
    __CLASS_MAPPING = {
        PlayerTypes.Remote: RemotePlayer,
        PlayerTypes.Bot: BotPlayer,
        PlayerTypes.Observer: Observer
    }

    @staticmethod
    def create_player(player_type: PlayerTypes,
                      turn_played_sem: Semaphore,
                      current_player_idx: list[int],
                      over: Event,
                      name: str | None = None,
                      password: str | None = None,
                      is_observer: bool | None = None,
                      current_turn: list[int] = None) -> Player:
        player_class = PlayerFactory.__CLASS_MAPPING[player_type]
        return player_class(name=name,
                            password=password,
                            is_observer=is_observer,
                            turn_played_sem=turn_played_sem,
                            current_player=current_player_idx,
                            over=over,
                            current_turn=current_turn)
