from threading import Event, Semaphore
from typing import Callable

from client.server_enum import Action
from entity.tanks.tank import Tank
from map.hex import Hex
from map.map import Map
from player.player import Player


class RemotePlayer(Player):
    def __init__(self, name: str, password: str, is_observer: bool, turn_played_sem: Semaphore,
                 current_player: list[1], player_index: int, over: Event):
        super().__init__(name=name,
                         password=password,
                         is_observer=is_observer,
                         turn_played_sem=turn_played_sem,
                         current_player=current_player,
                         player_index=player_index,
                         over=over)

        self.__result_vtp: dict[Action, Callable] | None = None

    def add_map(self, game_map: Map):
        # Vector table pointer for mapping actions to their respective handlers
        self.__result_vtp = {
            Action.MOVE: game_map.local_move,
            Action.SHOOT: game_map.td_shoot
        }
        super().add_map(game_map)

    def _make_turn_plays(self) -> None:
        # force a turn first to make sure the game actions are correct
        # a.k.a. wait on a barrier
        self._game_client.force_turn()

        game_actions: dict = self._game_client.get_game_actions()

        for game_action in game_actions["actions"]:
            if game_action["player_id"] != self.idx:
                continue

            action: Action = game_action["action_type"]
            data: dict = game_action["data"]
            vehicle_id: str = data["vehicle_id"]
            print(vehicle_id)

            tank: Tank = self._map.get_tank(vehicle_id)
            target: tuple = Hex.unpack_coords(data["target"])

            self.__result_vtp[action](tank, target)
