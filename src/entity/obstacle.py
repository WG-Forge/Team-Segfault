from abc import ABC

from entity import Entity


class Obstacle(Entity, ABC):

    def __init__(self):
        super().__init__("obstacle")
