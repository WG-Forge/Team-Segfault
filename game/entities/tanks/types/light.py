from constants import LT_IMAGE_PATH
from entities.tanks.tank import Tank
from game_map.hex import Hex


class LightTank(Tank):
    __sp: int = 3  # Speed Points
    __dp: int = 1  # Destruction Points
    __max_range: int = 2  # Manhattan max range
    __min_range: int = 2  # Manhattan min range
    __fire_deltas: tuple = Hex.fire_deltas(__min_range, __max_range)

    def __init__(self, tank_id: int, tank_info: dict, colour: str, player_index: int):
        super().__init__(tank_id, tank_info, colour, player_index, LT_IMAGE_PATH)

    def coords_in_range(self) -> tuple:
        return tuple(Hex.coord_sum(delta, self._coord) for delta in LightTank.__fire_deltas)

    def shot_moves(self, target: tuple) -> tuple:
        # returns coords to where "self" can move shoot "target", ordered from closest to furthest away from "self"
        fire_locs_around_enemy = Hex.possible_shots(target, LightTank.__fire_deltas)
        sorted_fire_locs = sorted(fire_locs_around_enemy, key=lambda loc: Hex.manhattan_dist(self._coord, loc))
        return tuple(sorted_fire_locs)

    def is_too_far(self, target: tuple) -> bool:
        # True if too far to shoot, Null if just right, False if too close
        distance = Hex.manhattan_dist(self._coord, target)
        if distance > LightTank.__max_range:
            return True
        if distance < LightTank.__min_range:
            return False

    def possible_shots(self) -> tuple:
        x, y, z = self._coord
        return tuple([(dx + x, dy + y, dz + z) for (dx, dy, dz) in LightTank.__fire_deltas])

    def get_speed(self) -> int:
        return self.__sp

    def get_fire_deltas(self) -> tuple:
        return LightTank.__fire_deltas

    def fire_corridors(self) -> tuple:
        return ()

    def td_shooting_coord(self, target: tuple) -> tuple:
        return ()
