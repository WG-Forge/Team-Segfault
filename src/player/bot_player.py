from abc import ABC

from src.entity.tank import Tank
from src.player.player import Player


class BotPlayer(Player, ABC):
    def __init__(self, name: str, password: str = None, is_observer: bool = None):
        super().__init__(name, password, is_observer)
        self.__current_tank: int = 0

    def play_move(self) -> ([], []):
        # tank_id = self._tanks[self.__get_next_tank()].get_id()
        #
        # path = self._game_map.shortest_path(self._game_map.get_tank_position(tank_id), self._game_map.get_base()[0])
        #
        # next_hex_coords: []
        # if len(path) >= 3 and not isinstance(self._game_map.get_entity_at(path[2]), Tank):
        #     next_hex_coords = path[2].get_coordinates()
        # elif len(path) >= 2 and not isinstance(self._game_map.get_entity_at(path[1]), Tank):
        #     next_hex_coords = path[1].get_coordinates()
        # else:
        #     return {}, {}
        #
        # d: dict = {
        #     "vehicle_id": tank_id,
        #     "target": {
        #         "x": next_hex_coords[0],
        #         "y": next_hex_coords[1],
        #         "z": next_hex_coords[2]
        #     }
        # }
        #
        # return [d], []
        moves, shoots = [], []
        free_base_hexes = self._game_map.get_base().copy()
        for tank in self._tanks:
            if self._game_map.is_tank_in_base(tank.get_id()):
                continue

            tank_pos = self._game_map.get_tank_position(tank.get_id())
            closest_base_hex, closest_base_hex_distance = None, float('inf')
            for base_hex in free_base_hexes:
                if isinstance(self._game_map.get_entity_at(base_hex), Tank):
                    free_base_hexes.remove(base_hex)
                    continue
                if base_hex - tank_pos <= closest_base_hex_distance:
                    closest_base_hex_distance = base_hex - tank_pos
                    closest_base_hex = base_hex

            if closest_base_hex is not None:
                free_base_hexes.remove(closest_base_hex)
                path = self._game_map.shortest_path(tank_pos, closest_base_hex)
                next_hex_coords: []
                if len(path) >= 3 and not isinstance(self._game_map.get_entity_at(path[2]), Tank):
                    next_hex_coords = path[2].get_coordinates()
                elif len(path) >= 2 and not isinstance(self._game_map.get_entity_at(path[1]), Tank):
                    next_hex_coords = path[1].get_coordinates()
                else:
                    continue
                moves.append({
                    "vehicle_id": tank.get_id(),
                    "target": {
                        "x": next_hex_coords[0],
                        "y": next_hex_coords[1],
                        "z": next_hex_coords[2]}})
                self._game_map.update({"actions": [{"action_type": 101, "data": moves[len(moves) - 1]}]})
        return moves, shoots

    def __get_next_tank(self):
        # Get next tank using FIFO algorithm
        next_tank: int = self.__current_tank
        self.__current_tank += 1
        self.__current_tank %= len(self._tanks)
        return next_tank
