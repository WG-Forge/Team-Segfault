from constants import BASE_COLOR
from entity.entity_enum import Entities
from entity.map_features.feature import Feature


class Base(Feature):
    def __init__(self, coord: tuple):
        super().__init__(Entities.BASE, coord, BASE_COLOR)
