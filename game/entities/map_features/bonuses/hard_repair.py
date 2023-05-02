from constants import EMPTY_COLOR
from entities.entity import Entities
from entities.map_features.feature import Feature


class HardRepair(Feature):
    __can_be_used_by_types = (Entities.HEAVY_TANK, Entities.TANK_DESTROYER)

    def __init__(self, coord):
        super().__init__(Entities.HARD_REPAIR, coord, color=EMPTY_COLOR)

    def is_usable(self, tank_type: str) -> bool:
        if tank_type in self.__can_be_used_by_types:
            return True
        else:
            return False
