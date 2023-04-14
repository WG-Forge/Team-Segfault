from abc import ABC

from game.entity.entity import Entity


class LightRepair(Entity, ABC):

    def __init__(self):
        super().__init__("light_repair")
