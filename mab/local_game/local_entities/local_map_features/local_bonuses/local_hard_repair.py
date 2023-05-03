from local_constants import EMPTY_COLOR
from local_entities.local_entity import LocalEntities
from local_entities.local_map_features.local_feature import Feature


class LocalHardRepair(Feature):
    can_be_used_by: tuple = (LocalEntities.HEAVY_TANK, LocalEntities.TANK_DESTROYER)

    def __init__(self, coord):
        super().__init__(LocalEntities.HARD_REPAIR, coord, color=EMPTY_COLOR)

    def is_usable(self, tank_type: str) -> bool:
        if tank_type in self.can_be_used_by:
            return True
        else:
            return False
