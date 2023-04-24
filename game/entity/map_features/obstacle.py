from constants import OBSTACLE_COLOR
from entity.map_features.feature import Feature


class Obstacle(Feature):
    def __init__(self, coord: tuple):
        super().__init__('obstacle', coord, OBSTACLE_COLOR)
