from constants import DEFAULT_SPAWN_COLOR
from entities.map_features.feature import Feature
from entities.entity_enum import Entities


class Spawn(Feature):
    def __init__(self, coord: tuple, tank_id: int = -1, color: tuple = DEFAULT_SPAWN_COLOR):
        self.__belongs_to = tank_id
        super().__init__(Entities.SPAWN, coord, color)

    def get_belongs_id(self) -> int:
        return self.__belongs_to
