from abc import ABC

from ..entity import Entity


class HardRepair(Entity, ABC):

    def __init__(self):
        super().__init__("hard_repair")
