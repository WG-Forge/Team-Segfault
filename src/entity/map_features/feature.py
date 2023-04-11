from abc import ABC

from entity.entity import Entity
from map.hex import Hex


class Feature(Entity, ABC):
    def __init__(self, name: str, coord: tuple):
        self.__corners = Hex.make_corners(coord)
        self.__center = Hex.make_center(coord)
        super().__init__(name)

    def get_corners(self) -> tuple:
        return self.__corners

    def get_center(self) -> tuple:
        return self.__center
