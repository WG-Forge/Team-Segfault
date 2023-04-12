from abc import ABC

from entity.map_features.feature import Feature


class Base(Feature, ABC):
    color = 'green'

    def __init__(self, coord: tuple):
        super().__init__('base', coord, Base.color)
