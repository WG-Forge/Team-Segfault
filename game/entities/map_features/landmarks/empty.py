from constants import EMPTY_COLOR
from entities.entity_enum import Entities
from entities.map_features.feature import Feature


class Empty(Feature):
    def __init__(self, coord: tuple):
        super().__init__(Entities.EMPTY, coord, EMPTY_COLOR)
