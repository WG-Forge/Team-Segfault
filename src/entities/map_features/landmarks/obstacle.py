from src.constants import OBSTACLE_COLOR
from src.entities.entity_enum import Entities
from src.entities.map_features.feature import Feature


class Obstacle(Feature):
    def __init__(self, coord: tuple):
        super().__init__(Entities.OBSTACLE, coord, OBSTACLE_COLOR)
