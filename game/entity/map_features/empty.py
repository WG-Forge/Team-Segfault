from constants import EMPTY_COLOR
from entity.map_features.feature import Feature


class Empty(Feature):

    def __init__(self, coord: tuple):
        super().__init__('empty', coord, EMPTY_COLOR)
