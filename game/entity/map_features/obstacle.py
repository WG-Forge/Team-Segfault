from abc import ABC

from entity.map_features.feature import Feature


class Obstacle(Feature, ABC):
    color = (51, 46, 46)  # dark red

    def __init__(self, coord: tuple):
        super().__init__('obstacle', coord, Obstacle.color)
