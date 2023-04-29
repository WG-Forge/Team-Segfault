from abc import ABC

from entities.entity import Entity, Entities
from game_map.hex import Hex


class Feature(Entity, ABC):
    """ Abstract feature class """

    def __init__(self, name: Entities, coord: tuple, color):
        self.__corners: tuple = Hex.make_corners(coord)
        self.__center: tuple = Hex.make_center(coord)
        self.__color = color
        super().__init__(name)

    @property
    def corners(self) -> tuple:
        return self.__corners

    @property
    def center(self) -> tuple:
        return self.__center

    @property
    def color(self) -> tuple:
        return self.__color
