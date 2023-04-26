from constants import TD_IMAGE_PATH
from entity.tanks.tank import Tank
from map.hex import Hex


class TankDestroyer(Tank):
    __sp: int = 1  # Speed Points
    __dp: int = 2  # Destruction Points
    __max_range: int = 3  # Manhattan max range
    __min_range: int = 1  # Manhattan min range
    # Creates fire deltas normally but avoids adding coords which don't contain 0s creating the TDs fire pattern
    __fire_deltas = tuple(coord for coord in Hex.fire_deltas(__min_range, __max_range) if 0 in coord)
    __fire_corridor_deltas: tuple = Hex.td_fire_corridor_deltas(__max_range)

    def __init__(self, tank_id: int, tank_info: dict, colour: str, player_index: int):
        super().__init__(tank_id, tank_info, colour, player_index, TD_IMAGE_PATH)

    def coords_in_range(self) -> tuple:
        return tuple(Hex.coord_sum(delta, self._coord) for delta in TankDestroyer.__fire_deltas)

    def shot_moves(self, target: tuple) -> tuple:
        # returns coords to where "self" can move shoot "target", ordered from closest to furthest away from "self"
        fire_locs_around_enemy = Hex.possible_shots(target, TankDestroyer.__fire_deltas)
        sorted_fire_locs = sorted(fire_locs_around_enemy, key=lambda loc: Hex.manhattan_dist(self._coord, loc))
        return tuple(sorted_fire_locs)

    def is_too_far(self, target: tuple) -> bool:
        # True if too far to shoot, Null if just right, False if too close
        distance = Hex.manhattan_dist(self._coord, target)
        if distance > TankDestroyer.__max_range:
            return True
        if distance < TankDestroyer.__min_range:
            return False

    def possible_shots(self) -> tuple:
        x, y, z = self._coord
        return tuple([(dx + x, dy + y, dz + z) for (dx, dy, dz) in TankDestroyer.__fire_deltas])

    def get_speed(self) -> int:
        return self.__sp

    def get_fire_deltas(self) -> tuple:
        return TankDestroyer.__fire_deltas

    def fire_corridors(self) -> tuple:
        return tuple([tuple([Hex.coord_sum(self._coord, delta) for delta in corridor_deltas]) for corridor_deltas in
                      TankDestroyer.__fire_corridor_deltas])

    def td_shooting_coord(self, target: tuple) -> tuple:
        # Returns the coord where the TD needs to fire to, to hit the tank in 'target' ('target' is in TD fire pattern)
        distance = Hex.manhattan_dist(self._coord, target)
        if distance == 1: return target
        return Hex.coord_sum(target, Hex.coord_mult(Hex.dir_vec(target, self._coord), distance - 1))
