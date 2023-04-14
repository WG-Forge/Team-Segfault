from abc import ABC

from map.hex import Hex
from ..entity import Entity


class Feature(Entity, ABC):
    def __init__(self, name: str, coord: tuple, color: str):
        self.__corners = Hex.make_corners(coord)
        self.__center = Hex.make_center(coord)
        self.__color = color
        super().__init__(name)

    def get_corners(self) -> tuple:
        return self.__corners

    def get_center(self) -> tuple:
        return self.__center

    def get_color(self) -> str:
        return self.__color
