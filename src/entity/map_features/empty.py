from abc import ABC

from entity.map_features.feature import Feature


class Empty(Feature, ABC):
    __color = 'black'

    def __init__(self, coord: tuple):
        super().__init__('empty', coord)

    def get_color(self) -> str:
        return Empty.__color
