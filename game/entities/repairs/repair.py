from abc import ABC

from entities.entity import Entity
from entities.entity_enum import Entities


class Repair(Entity, ABC):

    def __init__(self, name: Entities):
        super().__init__(name)
