from constants import OBSTACLE_COLOR
from entities.entity_enum import Entities
from entities.map_features.feature import Feature


class Obstacle(Feature):
    def __init__(self, coord: tuple):
        super().__init__(Entities.OBSTACLE, coord, OBSTACLE_COLOR)
