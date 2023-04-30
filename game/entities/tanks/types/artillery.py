from abc import ABC
from typing import Union, Dict, Tuple

from constants import SPG_IMAGE_PATH
from entities.map_features.bonuses.catapult import get_catapult_bonus_range
from entities.tanks.tank import Tank
from game_map.hex import Hex


class Artillery(Tank, ABC):
    __sp: int = 1  # Speed Points
    __dp: int = 1  # Destruction Points
    __max_range: int = 3  # Manhattan max range
    __min_range: int = 3  # Manhattan min range
    __catapult_range: int = __max_range + get_catapult_bonus_range()  # Manhattan max range when in catapult hex

    __fire_deltas: Tuple = Hex.fire_deltas(__min_range, __max_range)
    __catapult_deltas: Tuple = Hex.fire_deltas(__max_range, __catapult_range)
    __all_deltas: Tuple = __fire_deltas + __catapult_deltas

    def __init__(self, tank_id: int, tank_info: Dict, colour: Tuple, player_index: int, catapult_coords: Tuple):
        super().__init__(tank_id, tank_info, colour, player_index, SPG_IMAGE_PATH, catapult_coords)

    def coords_in_range(self, is_on_catapult: bool) -> Tuple:
        if is_on_catapult:
            deltas = self.__all_deltas
        else:
            deltas = self.__fire_deltas
        return tuple(Hex.coord_sum(delta, self._coord) for delta in deltas)

    def shot_moves(self, target: Tuple) -> Tuple:
        # returns coords to where "self" can move shoot "target", ordered from closest to furthest away from "self"
        fire_locs_around_enemy = Hex.possible_shots(target, self.__fire_deltas)
        sorted_fire_locs = sorted(fire_locs_around_enemy, key=lambda loc: Hex.manhattan_dist(self._coord, loc))
        return tuple(sorted_fire_locs)

    def catapult_shot_moves(self, target: Tuple) -> Tuple:
        cat_locs_around_enemy = Hex.possible_shots(target, self.__catapult_deltas)
        sorted_cat_locs = sorted(cat_locs_around_enemy, key=lambda loc: Hex.manhattan_dist(self._coord, loc))
        return tuple(sorted_cat_locs)

    def fire_corridors(self) -> tuple: return ()

    def td_shooting_coord(self, target: tuple) -> tuple: return ()

    @property
    def speed(self) -> int: return self.__sp
