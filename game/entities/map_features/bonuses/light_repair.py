from constants import EMPTY_COLOR
from entities.entity import Entities
from entities.map_features.feature import Feature


class LightRepair(Feature):
    __can_be_used_by_type = Entities.MEDIUM_TANK

    def __init__(self, coord):
        super().__init__(Entities.LIGHT_REPAIR, coord, color=EMPTY_COLOR)

    def is_usable(self, tank_type: str) -> bool:
        if tank_type == self.__can_be_used_by_type:
            return True
        else:
            return False
