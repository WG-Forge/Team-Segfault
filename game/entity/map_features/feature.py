from entity.entity import Entity
from map.hex import Hex


class Feature(Entity):
    """ Abstract feature class """

    def __init__(self, name: str, coord: tuple, color):
        self.__corners: tuple = Hex.make_corners(coord)
        self.__center: tuple = Hex.make_center(coord)
        self.__color = color
        super().__init__(name)

    def get_corners(self) -> tuple:
        return self.__corners

    def get_center(self) -> tuple:
        return self.__center

    def get_color(self) -> tuple:
        return self.__color
