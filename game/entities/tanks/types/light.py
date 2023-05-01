from abc import ABC

from constants import LT_IMAGE_PATH
from entities.map_features.bonuses.catapult import get_catapult_bonus_range
from entities.tanks.tank import Tank
from game_map.hex import Hex


class LightTank(Tank, ABC):
    __sp: int = 3  # Speed Points
    __dp: int = 1  # Destruction Points
    __max_range: int = 2  # Manhattan max range
    __min_range: int = 2  # Manhattan min range
    __catapult_range: int = __max_range + get_catapult_bonus_range()  # Manhattan max range when in catapult hex

    __fire_deltas: tuple = Hex.fire_deltas(__min_range, __max_range)
    __catapult_deltas: tuple = Hex.fire_deltas(__max_range, __catapult_range)
    __all_deltas: tuple = __fire_deltas + __catapult_deltas

    def __init__(self, tank_id: int, tank_info: dict, colour: tuple, player_index: int, catapult_coords: tuple):
        super().__init__(tank_id, tank_info, colour, player_index, LT_IMAGE_PATH, catapult_coords)

    def coords_in_range(self, is_on_catapult: bool) -> tuple:
        if is_on_catapult:
            deltas = self.__all_deltas
        else:
            deltas = self.__fire_deltas
        return tuple(Hex.coord_sum(delta, self._coord) for delta in deltas)

    def shot_moves(self, target: tuple) -> tuple:
        # returns coords to where "self" can move shoot "target", ordered from closest to furthest away from "self"
        fire_locs_around_enemy = Hex.possible_shots(target, LightTank.__fire_deltas)
        sorted_fire_locs = sorted(fire_locs_around_enemy, key=lambda loc: Hex.manhattan_dist(self._coord, loc))
        return tuple(sorted_fire_locs)

    def possible_shots(self) -> tuple:
        x, y, z = self._coord
        return tuple([(dx + x, dy + y, dz + z) for (dx, dy, dz) in LightTank.__fire_deltas])

    def fire_corridors(self) -> tuple:
        return ()

    def td_shooting_coord(self, target: tuple) -> tuple:
        return ()

    @property
    def speed(self) -> int:
        return self.__sp
