import os
from threading import Event

import pygame
from pygame import Surface

from consts import FPS_MAX, SCREEN_WIDTH, SCREEN_HEIGHT

os.environ['SDL_VIDEO_CENTERED'] = '1'  # window at center


class EndScreen:
    def __init__(self, active: Event):
        super().__init__()

        pygame.init()

        self.__active = active

        pygame.display.set_caption("Game has just finished!")

        self.__screen: Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.__clock = pygame.time.Clock()

    def run(self) -> None:
        while self.__active.is_set():
            # handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__active.clear()

            # delay for a constant framerate
            self.__clock.tick(FPS_MAX)

        # cleanup
        pygame.quit()
