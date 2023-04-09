from abc import ABC
from typing import List

from entity.entity import Entity


class Base(Entity, ABC):
    def __init__(self, base_coords: dict):
        self.__base_coords: tuple = tuple(tuple(d.values()) for d in base_coords)
        self.__occupied_coords: List[bool] = [False] * len(self.__base_coords)
        super().__init__('base')

    def is_in(self, tank_coords: tuple) -> bool:
        return tank_coords in self.__base_coords

    def occupy(self, tank_coord: tuple) -> None:
        self.__occupied_coords[self.__base_coords.index(tank_coord)] = True

    def leave(self, tank_coord: tuple) -> None:
        self.__occupied_coords[self.__base_coords.index(tank_coord)] = False

    def get_coords(self) -> tuple:
        return self.__base_coords

    def get_free_coords(self) -> List:
        free_coords = []
        for i, coord in enumerate(self.__base_coords):
            if not self.__occupied_coords[i]:
                free_coords.append(coord)
        return free_coords
