from abc import ABC

from src.client.server_enum import Action
from src.entity.tank import Tank
from src.player.player import Player


class BotPlayer(Player, ABC):
    def __init__(self, name: str, password: str = None, is_observer: bool = None):
        super().__init__(name, password, is_observer)

    def play_move(self) -> (Action, dict):
        tank_id = self._tanks[0].get_id()
        path = self._game_map.shortest_path(self._game_map.get_tank_position(tank_id), self._game_map.get_base()[0])
        next_hex_coords: []
        if len(path) >= 3 and not isinstance(self._game_map.get_entity_at(path[2]), Tank):
            next_hex_coords = path[2].get_coordinates()
        elif len(path) >= 2 and not isinstance(self._game_map.get_entity_at(path[1]), Tank):
            next_hex_coords = path[1].get_coordinates()
        else:
            return {}, {}

        d: dict = {
            "vehicle_id": tank_id,
            "target": {
                "x": next_hex_coords[0],
                "y": next_hex_coords[1],
                "z": next_hex_coords[2]
            }
        }

        return d, {}
