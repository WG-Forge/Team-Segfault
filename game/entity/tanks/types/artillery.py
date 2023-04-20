from abc import ABC

from entity.tanks.tank import Tank
from map.hex import Hex


class Artillery(Tank, ABC):
    __sp: int = 1  # Speed Points
    __dp: int = 1  # Destruction Points
    __max_range = 3  # Manhattan max range
    __min_range = 3  # Manhattan min range
    __fire_deltas: tuple = Hex.fire_deltas(__min_range, __max_range)
    __symbol: str = 's'

    def __init__(self, tank_id: int, tank_info: dict, colour: str, player_index: int):
        image_path = 'game/assets/tank_classes/spg.png'
        super().__init__(tank_id, tank_info, colour, player_index, image_path)

    def shot_moves(self, target: tuple) -> tuple:
        # returns coords to where "self" can move shoot "target", ordered from closest to furthest away from "self"
        fire_locs_around_enemy = Hex.possible_shots(target, Artillery.__fire_deltas)
        sorted_fire_locs = sorted(fire_locs_around_enemy, key=lambda loc: Hex.manhattan_dist(self._coord, loc))
        return tuple(sorted_fire_locs)

    def is_too_far(self, target: tuple) -> bool:
        # True if too far to shoot, None if just right, False if too close
        distance = Hex.manhattan_dist(self._coord, target)
        if distance > Artillery.__max_range:
            return True
        if distance < Artillery.__min_range:
            return False

    def get_speed(self) -> int:
        return self.__sp

    def get_symbol(self) -> str:
        return Artillery.__symbol

    def get_fire_deltas(self) -> tuple:
        return Artillery.__fire_deltas
