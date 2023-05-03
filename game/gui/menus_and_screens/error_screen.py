import pygame
from pygame import Surface

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, MENU_FONT, WHITE


class ErrorScreen:
    def __init__(self, screen: Surface):
        self.__screen = screen

    def draw(self, text: str) -> None:
        self.__screen.blit(pygame.font.Font(MENU_FONT, SCREEN_WIDTH / 10).render(text, True, WHITE), SCREEN_HEIGHT / 2)
