from threading import Event, Semaphore
from typing import Callable

from client.server_enum import Action
from entity.tanks.tank import Tank
from map.hex import Hex
from map.map import Map
from player.player import Player


class RemotePlayer(Player):

    def __init__(self, turn_played_sem: Semaphore,
                 current_player: list[1], player_index: int, active: Event):
        super().__init__(turn_played_sem, current_player, player_index, active)

        self.__result_vtp: dict[Action, Callable] | None = None

    def add_map(self, game_map: Map):
        # Vector table pointer for mapping actions to their respective handlers
        self.__result_vtp = {
            Action.MOVE: game_map.local_move,
            Action.SHOOT: game_map.local_shoot
        }
        super().add_map(game_map)

    def _make_turn_plays(self) -> None:
        game_actions: dict = self._game_client.get_game_actions()

        for game_action in game_actions["actions"]:
            if game_action["player_id"] != self.idx:
                continue

            action: Action = game_action["action_type"]
            data: dict = game_action["data"]
            vehicle_id: int = data["vehicle_id"]
            target: tuple = Hex.unpack_coords(data["target"])

            tank: Tank = self._tank_map[vehicle_id]

            self.__result_vtp[action](tank, target)
