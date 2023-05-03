from local_constants import OBSTACLE_COLOR
from local_entities.local_entity_enum import LocalEntities
from local_entities.local_map_features.local_feature import Feature


class LocalObstacle(Feature):
    def __init__(self, coord: tuple):
        super().__init__(LocalEntities.OBSTACLE, coord, OBSTACLE_COLOR)
