from abc import abstractmethod

import pygame
from pygame import Surface

from entity.entity import Entity
from map.hex import Hex


class Tank(Entity):
    __damage = 1

    def __init__(self, tank_id: int, tank_info: dict, colour: str, player_index: int, image_path: str):
        self.__tank_id = tank_id
        self.__hp: int = tank_info["health"]
        self.__og_hp: int = self.__hp
        self.__cp = tank_info["capture_points"]
        self.__spawn_coord: tuple = (tank_info["position"]["x"], tank_info["position"]["y"], tank_info["position"]["z"])
        self.__tank_colour: str = colour
        self.__player_index: int = player_index
        self.__destroyed: bool = False
        self.__image: Surface = pygame.image.load(image_path)
        self.__screen_position = (-1, -1)

        self._coord: tuple = self.__spawn_coord

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
        self.__hp -= Tank.__damage  # All tanks do 1 damage
        if self.__hp < 1:
            self.__destroyed = True
        return self.__destroyed

    def respawn(self) -> None:
        self.__destroyed = False
        self.__hp = self.__og_hp

    """     GETTERS     """

    def get_coord(self) -> tuple: return self._coord

    def get_player_index(self) -> int: return self.__player_index

    def get_id(self) -> int: return self.__tank_id

    def get_color(self) -> str: return self.__tank_colour

    def get_hp(self) -> int: return self.__hp

    def is_destroyed(self) -> bool: return self.__destroyed

    def get_cp(self) -> int: return self.__cp

    def get_spawn_coord(self) -> tuple: return self.__spawn_coord

    """     SETTERS     """

    def set_coord(self, new_coord: tuple) -> None: self._coord = new_coord

    def set_hp(self, hp: int): self.__hp = hp

    def set_cp(self, capture_pts: int): self.__cp = capture_pts

    """     ABSTRACTS       """

    @abstractmethod
    def shot_moves(self, target: tuple) -> tuple: pass  # sorted coords to where "self" can move to shoot "target"

    def get_screen_position(self) -> (int, int):
        return self.__screen_position

    @abstractmethod
    def get_symbol(self) -> str: pass

    @abstractmethod
    def get_speed(self) -> int: pass

    @abstractmethod
    def is_too_far(self, target: tuple) -> bool: pass  # True: too far to shoot, Null: just right, False: too close

    @abstractmethod
    def get_fire_deltas(self) -> tuple: pass
