from abc import ABC
from mab.local_game.local_entities.local_entity_enum import LocalEntities


# Entity - Abstract Base Class
class LocalEntity(ABC):
    def __init__(self, name: LocalEntities):
        self._type: LocalEntities = name

    @property
    def type(self) -> LocalEntities:
        return self._type
