from constants import BASE_COLOR
from entity.map_features.feature import Feature


class Base(Feature):
    def __init__(self, coord: tuple):
        super().__init__('base', coord, BASE_COLOR)
