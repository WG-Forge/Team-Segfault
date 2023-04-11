from abc import ABC

from entity.map_features.feature import Feature


class Base(Feature, ABC):
    __color = 'green'

    def __init__(self, coord: tuple):
        super().__init__('base', coord)

    def get_color(self) -> str:
        return Base.__color
