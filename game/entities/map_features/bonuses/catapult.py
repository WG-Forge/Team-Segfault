from constants import EMPTY_COLOR
from entities.entity import Entities
from entities.map_features.feature import Feature


class Catapult(Feature):
    bonus_range = 1  # Manhattan distance by which this bonus increases range

    def __init__(self, coord):
        super().__init__(Entities.CATAPULT, coord, color=EMPTY_COLOR)
        self.__remaining_uses = 3

    def is_usable(self, tank_type: str) -> bool:
        if self.__remaining_uses > 0:
            return True
        else:
            return False

    def was_used(self) -> None:
        self.__remaining_uses -= 1
        print('__remaining_uses', self.__remaining_uses)


def get_catapult_bonus_range() -> int:
    return Catapult.bonus_range
