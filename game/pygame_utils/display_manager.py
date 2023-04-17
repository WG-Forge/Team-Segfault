import os
from threading import Event

import pygame
from pygame import Surface

from consts import FPS_MAX
from map.map import Map

os.environ['SDL_VIDEO_CENTERED'] = '1'  # window at center


class DisplayManager:
    def __init__(self, active: Event, game_map: Map, width: int = 800, height: int = 600):
        super().__init__()

        pygame.init()

        self.__active = active
        self.__game_map = game_map

        pygame.display.set_caption("Tank game")

        self.__screen: Surface = pygame.display.set_mode((width, height))
        self.__clock = pygame.time.Clock()

    def run(self) -> None:
        while self.__active.is_set():
            # handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__active.clear()

            # draw the map
            self.__game_map.draw(self.__screen)

            # delay for a constant framerate
            self.__clock.tick(FPS_MAX)

        # cleanup
        pygame.quit()
