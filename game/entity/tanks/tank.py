from abc import ABC, abstractmethod

import pygame
from pygame import Surface

from entity.entity import Entity
from map.hex import Hex


class Tank(Entity, ABC):
    __damage = 1

    def __init__(self, tank_id: int, tank_info: dict, colour: str, player_index: int):
        self.__coord = None
        self.__tank_id = tank_id
        self.__hp: int = tank_info["health"]
        self.__og_hp: int = self.__hp
        self.__cp = tank_info["capture_points"]
        self.__spawn_coord: tuple = (tank_info["position"]["x"], tank_info["position"]["y"], tank_info["position"]["z"])
        self._coord: tuple = self.__spawn_coord
        self.__tank_colour: str = colour
        self.__player_index: int = player_index

        super().__init__(tank_info["vehicle_type"])

    def draw(self, screen: Surface) -> None:
        x, y = Hex.make_center(self._coord)
        shape_corners, is_closed = self.get_tank_type_shape(x, y, Hex.radius_x, Hex.radius_y)
        if shape_corners is None:
            return

        shape_corners = [(screen.get_width() // 2 + round(x * Hex.radius_x),
                          screen.get_height() // 2 - round(y * Hex.radius_y)) for x, y in shape_corners]

        # draw tank shape
        if is_closed:
            pygame.draw.polygon(screen, self.__tank_colour, shape_corners)
        else:
            for i in range(len(shape_corners) // 2):
                pygame.draw.line(screen, self.__tank_colour, start_pos=shape_corners[2 * i],
                                 end_pos=shape_corners[2 * i + 1], width=3)

        # show tank HP
        font_size = round(1.2 * min(Hex.radius_y, Hex.radius_x))
        font = pygame.font.SysFont('arial', font_size, bold=True)
        text = font.render(str(self.__hp), True, (0, 0, 0))
        screen.blit(text, dest=(screen.get_width() // 2 + round(x * Hex.radius_x),
                                screen.get_height() // 2 - round(y * Hex.radius_y) - font_size / 2))

    def update_hp(self, hp: int):
        self.__hp = hp

    def update_cp(self, capture_pts: int):
        self.__cp = capture_pts

    def register_hit_return_destroyed(self) -> bool:
        self.__hp -= 1  # All tanks do 1 damage
        if self.__hp < 1:
            self.__hp = self.__og_hp
            return True
        return False

    def get_spawn_coord(self) -> tuple:
        return self.__spawn_coord

    def get_id(self) -> int:
        return self.__tank_id

    def get_player_index(self) -> int:
        return self.__player_index

    def get_color(self) -> str:
        return self.__tank_colour

    def get_coord(self) -> tuple:
        return self._coord

    def set_coord(self, new_coord: tuple) -> None:
        self._coord = new_coord

    def in_range(self, target: tuple) -> bool:
        return target in self.get_possible_shots()

    def get_hp(self) -> int:
        return self.__hp

    def get_cp(self) -> int:
        return self.__cp

    @abstractmethod
    def get_symbol(self) -> str:
        pass

    @abstractmethod
    def get_speed(self) -> int:
        pass

    @abstractmethod
    def get_possible_shots(self):
        pass

    @abstractmethod
    def get_tank_type_shape(self, x: int, y: int, radius_x: int, radius_y: int) -> ([], bool):
        """
        Returns the shape tank needs to be drawn like
        :param radius_y: y-radius of one hex
        :param radius_x: x-radius of one hex
        :param x: x coordinate in cartesian coordinate system
        :param y: y coordinate in cartesian coordinate system
        :return: (vertex coordinates of tank shape, if tank shape is closed polygon)
        """
        pass
