import os

import pygame

from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from game_map.hex import Hex

os.environ['SDL_VIDEO_CENTERED'] = '1'  # window at center


class EndScreen:
    @staticmethod
    def draw_podium(screen, players):
        screen.fill('blue')
        width = Hex.radius_x * 4
        third_height = Hex.radius_y * 2
        pygame.draw.rect(screen, 'grey', (SCREEN_WIDTH // 2 - width * 1.5, SCREEN_HEIGHT // 2 - third_height * 2,
                                          width, third_height * 2))
        pygame.draw.rect(screen, 'yellow', (SCREEN_WIDTH // 2 - width / 2, SCREEN_HEIGHT // 2 - 3 * third_height,
                                            width, third_height * 3))
        pygame.draw.rect(screen, 'brown', (SCREEN_WIDTH // 2 + width / 2, SCREEN_HEIGHT // 2 - third_height,
                                           width, third_height))
        for player in players:
            pass
