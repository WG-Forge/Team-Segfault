from abc import ABC

from entity.map_features.feature import Feature


class Empty(Feature, ABC):
    color = 'black'

    def __init__(self, coord: tuple):
        super().__init__('empty', coord, Empty.color)