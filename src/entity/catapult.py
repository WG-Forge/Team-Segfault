from abc import ABC

from entity import Entity


class Catapult(Entity, ABC):
    def __init__(self):
        super().__init__("catapult")
