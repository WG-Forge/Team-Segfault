from src.constants import EMPTY_COLOR
from src.entities.entity import Entities
from src.entities.map_features.feature import Feature


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

def get_catapult_bonus_range() -> int:
    return Catapult.bonus_range
