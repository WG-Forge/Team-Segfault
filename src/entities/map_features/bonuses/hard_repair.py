from src.constants import EMPTY_COLOR
from src.entities.entity import Entities
from src.entities.map_features.feature import Feature


class HardRepair(Feature):
    can_be_used_by: tuple = (Entities.HEAVY_TANK, Entities.TANK_DESTROYER)

    def __init__(self, coord):
        super().__init__(Entities.HARD_REPAIR, coord, color=EMPTY_COLOR)

    def is_usable(self, tank_type: Entities) -> bool:
        return tank_type in HardRepair.can_be_used_by
