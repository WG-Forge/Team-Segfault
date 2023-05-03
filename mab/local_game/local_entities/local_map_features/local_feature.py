from abc import ABC

from local_entities.local_entity import LocalEntity, LocalEntities
from local_map.local_hex import LocalHex


class LocalFeature(LocalEntity, ABC):
    """ Abstract feature class """

    def __init__(self, name: LocalEntities, coord: tuple, color: tuple[int, int, int] | str):
        self.__corners: tuple = LocalHex.make_corners(coord)
        self.__center: tuple = LocalHex.make_center(coord)
        self.__color: tuple[int, int, int] | str = color
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
