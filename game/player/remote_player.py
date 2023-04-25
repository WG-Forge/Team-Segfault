from threading import Event, Semaphore
from typing import Callable

from client.server_enum import Action
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
        super().add_map(game_map)

    def _make_turn_plays(self) -> None:
        if self._current_player[0] == self.idx:
            self.__place_actions()

    def _finalize(self):
        # No need to do anything currently
        pass

    def __place_actions(self) -> None:

        # force the turn end first to make sure the game actions are correct
        self._game_client.force_turn()

        game_actions: dict = self._game_client.get_game_actions()
        action_dict = {}

        for game_action in game_actions["actions"]:
            action: Action = game_action["action_type"]
            data: dict = game_action["data"]
            vehicle_id: int = int(data["vehicle_id"])
            action_dict[vehicle_id] = data, action

        for tank in self._tanks:
            if not tank.get_id() in action_dict:
                continue

            data = action_dict[tank.get_id()][0]
            action = action_dict[tank.get_id()][1]
            target: tuple = Hex.unpack_coords(data["target"])

            if action == Action.SHOOT:
                if tank.get_type() == 'at_spg':
                    self._map.td_shoot(tank, target)
                else:
                    self._map.local_shoot_tuple(tank, target)
            else:
                self._map.local_move(tank, target)
