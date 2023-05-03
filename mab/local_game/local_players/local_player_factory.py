from enum import Enum
from threading import Semaphore, Event

from local_players.local_bot_player import LocalBotPlayer
from local_players.types.observer import Observer
from local_players.local_player import LocalPlayer
from local_players.types.remote_player import RemotePlayer


class LocalPlayerTypes(Enum):
    Remote = 1
    Bot = 2
    Observer = 3


class LocalPlayerFactory:
    __CLASS_MAPPING = {
        LocalPlayerTypes.Remote: RemotePlayer,
        LocalPlayerTypes.Bot: LocalBotPlayer,
        LocalPlayerTypes.Observer: Observer
    }

    @staticmethod
    def create_player(player_type: LocalPlayerTypes,
                      turn_played_sem: Semaphore,
                      current_player_idx: list[int],
                      over: Event,
                      name: str | None = None,
                      password: str | None = None,
                      is_observer: bool | None = None) -> LocalPlayer:
        player_class = LocalPlayerFactory.__CLASS_MAPPING[player_type]
        return player_class(name=name,
                            password=password,
                            is_observer=is_observer,
                            turn_played_sem=turn_played_sem,
                            current_player=current_player_idx,
                            over=over)
