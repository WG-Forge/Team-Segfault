from abc import ABC

from local_constants import SPG_IMAGE_PATH
from local_entities.local_map_features.local_bonuses.local_catapult import get_catapult_bonus_range
from local_entities.local_tanks.local_tank import LocalTank
from local_map.local_hex import LocalHex


class LocalArtillery(LocalTank, ABC):
    __speed_points: int = 1
    __damage_points: int = 1
    __max_range: int = 3  # Manhattan max range
    __min_range: int = 3  # Manhattan min range
    __catapult_range: int = __max_range + get_catapult_bonus_range()  # Manhattan max range when in catapult hex

    __fire_deltas: tuple = LocalHex.fire_deltas(__min_range, __max_range)
    __catapult_deltas: tuple = LocalHex.fire_deltas(__max_range, __catapult_range)
    __all_deltas: tuple = __fire_deltas + __catapult_deltas

    def __init__(self, tank_id: int, tank_info: dict, colour: tuple, player_index: int, catapult_coords: tuple):
        super().__init__(tank_id, tank_info, colour, player_index, SPG_IMAGE_PATH, catapult_coords)

    def coords_in_range(self, is_on_catapult: bool) -> tuple:
        if is_on_catapult:
            deltas = self.__all_deltas
        else:
            deltas = self.__fire_deltas
        return tuple(LocalHex.coord_sum(delta, self._coord) for delta in deltas)

    def shot_moves(self, target: tuple) -> tuple:
        if self._catapult_bonus:
            return self.__shot_moves(target, self.__catapult_deltas)
        return self.__shot_moves(target, self.__fire_deltas)

    def __shot_moves(self, target: tuple, deltas: tuple) -> tuple:
        # returns coords to where "self" can move shoot "target", ordered from closest to furthest away from "self"
        fire_locs_around_enemy = LocalHex.possible_shots(target, deltas)
        sorted_fire_locs = sorted(fire_locs_around_enemy, key=lambda loc: LocalHex.manhattan_dist(self._coord, loc))
        return tuple(sorted_fire_locs)

    def fire_corridors(self) -> tuple:
        return ()

    def td_shooting_coord(self, target: tuple) -> tuple:
        return ()

    @property
    def speed(self) -> int:
        return self.__speed_points
