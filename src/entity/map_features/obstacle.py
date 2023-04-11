from abc import ABC

from entity.map_features.feature import Feature


class Obstacle(Feature, ABC):
    __color = 'yellow'

    def __init__(self, coord: tuple):
        super().__init__('obstacle', coord)

    def get_color(self) -> str:
        return Obstacle.__color
