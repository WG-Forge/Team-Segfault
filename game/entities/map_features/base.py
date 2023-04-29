from constants import BASE_COLOR
from entities.map_features.feature import Feature
from entities.entity_enum import Entities


class Base(Feature):
    def __init__(self, coord: tuple):
        super().__init__(Entities.BASE, coord, BASE_COLOR)
