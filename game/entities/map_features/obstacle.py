from constants import OBSTACLE_COLOR
from entities.map_features.feature import Feature
from entities.entity_enum import Entities


class Obstacle(Feature):
    def __init__(self, coord: tuple):
        super().__init__(Entities.OBSTACLE, coord, OBSTACLE_COLOR)
