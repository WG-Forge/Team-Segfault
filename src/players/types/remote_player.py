from threading import Event, Semaphore

from src.entities.entity_enum import Entities
from src.game_map.hex import Hex
from src.game_map.map import Map
from src.players.player import Player
from src.remote.server_enum import Action


class RemotePlayer(Player):
    def __init__(self, turn_played_sem: Semaphore, current_player: list[int], over: Event,
                 name: str | None = None, password: str | None = None,
                 is_observer: bool | None = None):
        super().__init__(turn_played_sem=turn_played_sem, current_player=current_player, over=over,
                         name=name, password=password,
                         is_observer=is_observer)

    def add_map(self, game_map: Map) -> None:
        super().add_map(game_map)

    def _make_turn_plays(self) -> None:
        if self._current_player[0] == self.idx:
            self.__place_actions()

    def _finalize(self) -> None:
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
            if tank.tank_id not in action_dict:
                continue

            data = action_dict[tank.tank_id][0]
            action = action_dict[tank.tank_id][1]
            target: tuple = Hex.unpack_coords(data["target"])

            if action == Action.SHOOT:
                if tank.type == Entities.TANK_DESTROYER:
                    self._map.td_shoot(tank, target)
                else:
                    self._map.local_shoot_tuple(tank, target)
            else:
                self._map.local_move(tank, target)
