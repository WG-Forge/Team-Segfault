from abc import abstractmethod

import pygame
from pygame import Surface

from entity.entity import Entity
from map.hex import Hex


class Feature(Entity):
    """ Abstract feature class """

    def __init__(self, name: str, coord: tuple):
        self.__corners: tuple = Hex.make_corners(coord)
        self.__center: tuple = Hex.make_center(coord)
        super().__init__(name)

    def draw(self, screen: Surface, font_size=None) -> None:
        """Renders the hexagon on the screen and draw a border around the hexagon with the colour white"""
        corners = [(screen.get_width() // 2 + round(x * Hex.radius_x),
                    screen.get_height() // 2 - round(y * Hex.radius_y)) for x, y in self.__corners]
        pygame.draw.polygon(screen, self.get_color(), corners)
        pygame.draw.aalines(screen, (255, 255, 255), closed=True, points=corners)

    def get_corners(self) -> tuple:
        return self.__corners

    def get_center(self) -> tuple:
        return self.__center

    @abstractmethod
    def get_color(self) -> tuple:
        pass
