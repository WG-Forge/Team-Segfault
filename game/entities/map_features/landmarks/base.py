from constants import BASE_COLOR
from entities.entity_enum import Entities
from entities.map_features.feature import Feature


class Base(Feature):
    def __init__(self, coord: tuple):
        super().__init__(Entities.BASE, coord, BASE_COLOR)
