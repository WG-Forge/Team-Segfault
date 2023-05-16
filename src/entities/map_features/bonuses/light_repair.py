from src.constants import EMPTY_COLOR
from src.entities.entity import Entities
from src.entities.map_features.feature import Feature


class LightRepair(Feature):
    can_be_used_by: tuple = Entities.MEDIUM_TANK

    def __init__(self, coord):
        super().__init__(Entities.LIGHT_REPAIR, coord, color=EMPTY_COLOR)

    def is_usable(self, tank_type: Entities) -> bool:
        return tank_type in LightRepair.can_be_used_by
