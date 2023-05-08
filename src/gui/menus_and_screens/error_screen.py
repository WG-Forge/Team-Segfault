import pygame
from pygame import Surface

from src.constants import SCREEN_WIDTH, MENU_FONT, ERROR_FONT_SIZE, ERROR_MESSAGE_COLOR, HEX_RADIUS_Y


class ErrorScreen:
    def __init__(self):
        self.__enabled = False
        self.__error_message = ''
        self.__font = pygame.font.Font(MENU_FONT, ERROR_FONT_SIZE)

    def draw_error(self, screen: Surface):
        error_number, error_msg = str(self.__error_message).split(':')
        error_number = self.__font.render(error_number, True, ERROR_MESSAGE_COLOR)
        # error_msg = pygame.font.Font(MENU_FONT, ERROR_FONT_SIZE).render(error_msg, True, ERROR_MESSAGE_COLOR)
        screen.blit(error_number, ((SCREEN_WIDTH - error_number.get_width()) / 2, HEX_RADIUS_Y[0]))

        # split the text into lines
        words = error_msg.split()
        lines = []
        line = ""
        for word in words:
            if self.__font.size(line + " " + word)[0] < SCREEN_WIDTH:
                line += " " + word
            else:
                lines.append(line)
                line = word
        lines.append(line)

        # render each line of text
        y_offset = error_number.get_height() + HEX_RADIUS_Y[0]
        for line in lines:
            text_surface = self.__font.render(line, True, ERROR_MESSAGE_COLOR)
            text_rect = text_surface.get_rect()
            text_rect.center = (SCREEN_WIDTH // 2, y_offset)
            screen.blit(text_surface, text_rect)
            y_offset += self.__font.size(line)[1]

    def disable(self) -> None:
        self.__enabled = False

    def enable(self) -> None:
        self.__enabled = True

    def set_error_message(self, msg) -> None:
        self.__error_message = msg

    @property
    def enabled(self) -> bool:
        return self.__enabled
