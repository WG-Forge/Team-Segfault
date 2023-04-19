from abc import ABC, abstractmethod

import pygame
from pygame import Surface

from entity.entity import Entity
from map.hex import Hex


class Tank(Entity, ABC):
    __damage = 1

    def __init__(self, tank_id: int, tank_info: dict, colour: str, player_index: int, image_path: str):
        self.__coord = None
        self.__tank_id = tank_id
        self.__hp: int = tank_info["health"]
        self.__og_hp: int = self.__hp
        self.__cp = tank_info["capture_points"]
        self.__spawn_coord: tuple = (tank_info["position"]["x"], tank_info["position"]["y"], tank_info["position"]["z"])
        self._coord: tuple = self.__spawn_coord
        self.__tank_colour: str = colour
        self.__player_index: int = player_index
        self.__image: Surface = pygame.image.load(image_path)
        self.__screen_position = (-1, -1)

        super().__init__(tank_info["vehicle_type"])

    def draw(self, screen: Surface, font_size) -> None:
        x, y = Hex.make_center(self._coord)
        self.__screen_position = (screen.get_width() // 2 + round(x * Hex.radius_x) - 2 * Hex.radius_x // 3,
                                  screen.get_height() // 2 - round(y * Hex.radius_y) - 2 * Hex.radius_y // 3)
        # show tank sprite
        self.__image = pygame.transform.scale(self.__image, (Hex.radius_x * 1.5, Hex.radius_y * 1.5))
        color_image = pygame.Surface(self.__image.get_size())
        color_image.fill(self.__tank_colour)
        ti = self.__image.copy()
        ti.blit(color_image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(ti, self.__screen_position)

        # show tank HP
        font_size = round(1 * min(Hex.radius_y, Hex.radius_x))
        font = pygame.font.SysFont('arial', font_size, bold=True)
        text = font.render(str(self.__hp), True, 'white')
        screen.blit(text, dest=self.__screen_position)

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

    def get_screen_position(self) -> (int, int):
        return self.__screen_position

    @abstractmethod
    def get_symbol(self) -> str:
        pass

    @abstractmethod
    def get_speed(self) -> int:
        pass

    @abstractmethod
    def get_possible_shots(self):
        pass
