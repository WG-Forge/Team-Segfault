from abc import ABC
from typing import Dict, Tuple

from constants import TD_IMAGE_PATH
from entities.map_features.bonuses.catapult import get_catapult_bonus_range
from entities.tanks.tank import Tank
from game_map.hex import Hex


class TankDestroyer(Tank, ABC):
    __sp: int = 1  # Speed Points
    __dp: int = 2  # Destruction Points
    __max_range: int = 3  # Manhattan max range
    __min_range: int = 1  # Manhattan min range
    __catapult_range: int = __max_range + get_catapult_bonus_range()  # Manhattan max range when in catapult hex

    # Creates fire deltas normally but avoids adding coords which don't contain 0s creating the TDs fire pattern
    __fire_deltas = tuple(coord for coord in Hex.fire_deltas(__min_range, __max_range) if 0 in coord)
    __catapult_deltas = tuple(coord for coord in Hex.fire_deltas(__max_range, __catapult_range) if 0 in coord)

    __fire_corridor_deltas: tuple = Hex.td_fire_corridor_deltas(__max_range)
    __catapult_corridor_deltas: tuple = Hex.td_fire_corridor_deltas(__catapult_range)
    __all_deltas: Tuple = __fire_deltas + __catapult_deltas

    def __init__(self, tank_id: int, tank_info: Dict, colour: Tuple, player_index: int, catapult_coords: Tuple):
        super().__init__(tank_id, tank_info, colour, player_index, TD_IMAGE_PATH, catapult_coords)

    def coords_in_range(self, is_on_catapult: bool) -> Tuple:
        if is_on_catapult:
            deltas = self.__all_deltas
        else:
            deltas = self.__fire_deltas
        return tuple(Hex.coord_sum(delta, self._coord) for delta in deltas)

    def shot_moves(self, target: tuple) -> tuple:
        # returns coords to where "self" can move shoot "target", ordered from closest to furthest away from "self"
        fire_locs_around_enemy = Hex.possible_shots(target, TankDestroyer.__fire_deltas)
        sorted_fire_locs = sorted(fire_locs_around_enemy, key=lambda loc: Hex.manhattan_dist(self._coord, loc))
        return tuple(sorted_fire_locs)

    def possible_shots(self) -> tuple:
        x, y, z = self._coord
        return tuple([(dx + x, dy + y, dz + z) for (dx, dy, dz) in TankDestroyer.__fire_deltas])

    def fire_corridors(self) -> tuple:
        return tuple([tuple([Hex.coord_sum(self._coord, delta) for delta in corridor_deltas]) for corridor_deltas in
                      TankDestroyer.__fire_corridor_deltas])

    def td_shooting_coord(self, target: tuple) -> tuple:
        # Returns the coord where the TD needs to fire to, to hit the tank in 'target' ('target' is in TD fire pattern)
        distance = Hex.manhattan_dist(self._coord, target)
        if distance == 1: return target
        return Hex.coord_sum(target, Hex.coord_mult(Hex.dir_vec(target, self._coord), distance - 1))

    @property
    def speed(self) -> int: return self.__sp
