import math
from abc import ABC
from threading import Semaphore

from map.hex import Hex
from src.entity.tanks.tank import Tank
from src.player.player import Player


class BotPlayer(Player, ABC):
    def __init__(self, name: str, password: str, is_observer: bool,
                 turn_played_sem: Semaphore, current_player: list[1], player_index: int):
        super().__init__(name, password, is_observer, turn_played_sem, current_player, player_index)

    def move(self, who, where):
        pass

    def shoot(self, who, target):
        pass
    def _make_turn_plays(self) -> None:
        # tank movement order: SPGs, light tanks, heavy tanks, medium tanks, tank destroyers
        # TODO: fix this function so it moves tanks accordingly
        base = self._game_map.get_base()
        free_base_coords = base.get_free_coords()

        for tank in self._tanks:
            if base.is_in(tank):
                continue

            tank_pos = tank.get_pos()
            tank_coord = tank.get_coords()
            closest_base_coord, closest_base_dist = None, float('inf')
            for coord in free_base_coords:
                dist = self.distance(coord, tank_coord)
                if dist <= closest_base_dist:
                    closest_base_dist = dist
                    closest_base_coord = coord

            if closest_base_coord is not None:
                free_base_coords.remove(closest_base_coord)
                path = self._game_map.shortest_path(tank_pos, Hex(closest_base_coord))
                next_hex_coords: []
                # if len(path) >= 3 and not isinstance(self._game_map.get_entity_at(path[2]), Tank):
                #     next_hex_coords = path[2].get_coordinates()
                if len(path) >= 2 and not self._game_map.tank_in_pos(path[1]):
                    next_hex_coords = path[1].get_coords()
                else:
                    continue

                move = {
                    "vehicle_id": tank.get_id(),
                    "target": {
                        "x": next_hex_coords[0],
                        "y": next_hex_coords[1],
                        "z": next_hex_coords[2]}}

                self._game_client.move(move)
                self._game_map.update({"actions": [{"action_type": 101, "data": move}]})

    def distance(self, a: tuple, b: tuple):
        x1, y1, z1 = a
        x2, y2, z2 = b
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)