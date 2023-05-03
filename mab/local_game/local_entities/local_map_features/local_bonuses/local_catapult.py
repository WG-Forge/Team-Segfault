from local_constants import EMPTY_COLOR
from local_entities.local_entity import LocalEntities
from local_entities.local_map_features.local_feature import Feature


class LocalCatapult(Feature):
    bonus_range = 1  # Manhattan distance by which this bonus increases range

    def __init__(self, coord):
        super().__init__(LocalEntities.CATAPULT, coord, color=EMPTY_COLOR)
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
    return LocalCatapult.bonus_range
