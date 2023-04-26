from constants import EMPTY_COLOR
from entity.entity_enum import Entities
from entity.map_features.feature import Feature


class Empty(Feature):
    def __init__(self, coord: tuple):
        super().__init__(Entities.EMPTY, coord, EMPTY_COLOR)
