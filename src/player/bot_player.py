from abc import ABC

from src.client.server_enum import Action
from src.map.hex import Hex
from src.player.player import Player


class BotPlayer(Player, ABC):
    def __init__(self, name: str, password: str = None, is_observer: bool = None):
        super().__init__(name, password, is_observer)

    def play_move(self) -> (Action, dict):
        tank_id = self._tanks[0].get_id()
        path = self._game_map.shortest_path(self._game_map.get_tank_position(tank_id), Hex([0, 0, 0]))
        if len(path) == 1:
            return {}, {}
        next_hex_coords = (path[2] if len(path) >= 3 else path[1]).get_coordinates()

        d: dict = {
            "vehicle_id": tank_id,
            "target": {
                "x": next_hex_coords[0],
                "y": next_hex_coords[1],
                "z": next_hex_coords[2]
            }
        }
        print(d)
        # print(path[0], path[1])
        return d, {}
