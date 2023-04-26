from entity.entity_enum import Entities


class Entity:
    def __init__(self, name: Entities):
        self._type: Entities = name

    @property
    def type(self) -> Entities:
        return self._type
