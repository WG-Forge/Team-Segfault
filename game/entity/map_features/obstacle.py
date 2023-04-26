from constants import OBSTACLE_COLOR
from entity.entity_enum import Entities
from entity.map_features.feature import Feature


class Obstacle(Feature):
    def __init__(self, coord: tuple):
        super().__init__(Entities.OBSTACLE, coord, OBSTACLE_COLOR)
