from abc import ABC
from entities.entity_enum import Entities


# Entity - Abstract Base Class
class Entity(ABC):
    def __init__(self, name: Entities):
        self._type: Entities = name

    @property
    def type(self) -> Entities:
        return self._type
