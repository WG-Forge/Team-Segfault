from abc import ABC

from entity.entity import Entity
from map.hex import Hex


class Base(Entity, ABC):
    __color = 'green'

    def __init__(self, coord: tuple):
        self.__corners = Hex.make_corners(coord)
        self.__center = Hex.make_center(coord)
        super().__init__('base')

    def get_corners(self) -> tuple:
        return self.__corners

    def get_center(self) -> tuple:
        return self.__center

    def get_color(self) -> str:
        return Base.__color
