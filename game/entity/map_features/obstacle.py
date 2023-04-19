from abc import ABC

from entity.map_features.feature import Feature


class Obstacle(Feature, ABC):
    color = 'yellow'

    def __init__(self, coord: tuple):
        super().__init__('obstacle', coord, Obstacle.color)