import pygame
from pygame import Surface

from src.constants import SCREEN_WIDTH, MENU_FONT, ERROR_FONT_SIZE, ERROR_MESSAGE_COLOR, HEX_RADIUS_Y


class ErrorScreen:
    def __init__(self):
        self.__enabled = False
        self.__error_message = ''

    def draw_error(self, screen: Surface):
        error_number, error_msg = str(self.__error_message).split(':')
        error_number = pygame.font.Font(MENU_FONT, ERROR_FONT_SIZE).render(error_number, True, ERROR_MESSAGE_COLOR)
        error_msg = pygame.font.Font(MENU_FONT, ERROR_FONT_SIZE).render(error_msg, True, ERROR_MESSAGE_COLOR)
        screen.blit(error_number, ((SCREEN_WIDTH - error_number.get_width()) / 2, HEX_RADIUS_Y[0]))
        screen.blit(error_msg, ((SCREEN_WIDTH - error_msg.get_width()) / 2,
                                HEX_RADIUS_Y[0] + error_number.get_height()))

    def disable(self) -> None:
        self.__enabled = False

    def enable(self) -> None:
        self.__enabled = True

    def set_error_message(self, msg) -> None:
        self.__error_message = msg

    @property
    def enabled(self) -> bool:
        return self.__enabled
