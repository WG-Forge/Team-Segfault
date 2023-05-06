import pygame
from pygame import Surface

from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, TANK_ICON_PATH, PODIUM_COLORS, \
    PODIUM_WIDTH


class EndScreen:
    def __init__(self):
        self.__enabled = False
        self.__tank_image = pygame.transform.scale(pygame.image.load(TANK_ICON_PATH),
                                                   (PODIUM_WIDTH / 6, PODIUM_WIDTH / 6))
        width = PODIUM_WIDTH / 3
        third_height: int = PODIUM_WIDTH / 6
        max_y = SCREEN_HEIGHT / 2 + 1.5 * third_height
        self.__positions: list[tuple[int, int, int, int]] = [
            (SCREEN_WIDTH / 2 - width / 2, max_y - 3 * third_height, width, third_height * 3),
            (SCREEN_WIDTH / 2 - width * 1.5, max_y - 2 * third_height, width, third_height * 2),
            (SCREEN_WIDTH / 2 + width / 2, max_y - third_height, width, third_height)
        ]

    def draw_podium(self, screen: Surface, players: list[tuple[str, str | tuple[int, int, int], int]]):
        """
        Draws podium based on a given list of player names, colors and points. The list should be sorted by points
        :param Surface screen: screen to draw on
        :param list players: sorted list of players by points, where each element is a tuple(player_name, player_color,
        player_points)
        """
        for i in range(3):
            pygame.draw.rect(screen, PODIUM_COLORS[i], self.__positions[i])
        # todo: add names and points to podium
        if len(players) > 2 and players[0][2] == players[1][2]:
            pass
        else:
            for i, player in enumerate(players):
                img = self.__tank_image.copy()
                color_image = pygame.Surface(img.get_size())
                color_image.fill(player[1])
                img.blit(color_image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                screen.blit(img, dest=(self.__positions[i][0] + img.get_width() / 2,
                                       self.__positions[i][1] - img.get_height()))

    def toggle_enable(self) -> None:
        self.__enabled = not self.__enabled

    @property
    def enabled(self) -> bool:
        return self.__enabled
