from entities.map_features.feature import Feature
from entities.entity import Entities


class Catapult(Feature):
    bonus_range = 1  # Manhattan distance by which this bonus increases range

    def __init__(self, coord):
        super().__init__(Entities.CATAPULT, coord, color='red')
        self.__remaining_uses = 3

    def is_usable(self) -> bool:
        if self.__remaining_uses > 0:
            return True
        else:
            return False

    def was_used(self) -> None:
        self.__remaining_uses -= 1


def get_catapult_bonus_range() -> int:
    return Catapult.bonus_range
