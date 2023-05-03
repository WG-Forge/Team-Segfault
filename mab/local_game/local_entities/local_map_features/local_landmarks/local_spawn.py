from local_constants import DEFAULT_SPAWN_COLOR
from local_entities.local_entity_enum import LocalEntities
from local_entities.local_map_features.local_feature import Feature


class LocalSpawn(Feature):
    def __init__(self, coord: tuple, tank_id: int = -1, color: tuple = DEFAULT_SPAWN_COLOR):
        self.__belongs_to = tank_id
        super().__init__(LocalEntities.SPAWN, coord, color)

    def get_belongs_id(self) -> int:
        return self.__belongs_to
