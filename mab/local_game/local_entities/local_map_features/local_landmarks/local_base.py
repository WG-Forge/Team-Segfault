from local_constants import BASE_COLOR
from local_entities.local_entity_enum import LocalEntities
from local_entities.local_map_features.local_feature import Feature


class LocalBase(Feature):
    __rounds_to_cap = 1

    def __init__(self, coord: tuple):
        super().__init__(LocalEntities.BASE, coord, BASE_COLOR)