from enum import StrEnum

import pygame
import pygame_menu

from constants import MENU_POSITION, SOUND_VOLUME, PLAYER_NAMES, GAME_NAME, WHITE, MENU_BACKGROUND_COLOR, \
    MENU_SELECTED_TEXT_COLOR, GAME_SPEED, MENU_MIN_WIDTH, MENU_FONT


class GameType(StrEnum):
    LOCAL_MULTIPLAYER = 'Multiplayer'
    SINGLE_PLAYER = 'Local'
    PVP_MULTIPLAYER = 'PvP'
    SPECTATE = 'Spectate'


class Menu:
    def __init__(self, menu_width: int, menu_height: int, start_game_function):
        self.__menu_width = menu_width
        self.__menu_height = menu_height

        self.__create_menu_theme()
        # submenus need to be created before main menu
        self.__create_options_menu()
        self.__create_play_menu(start_game_function)
        self.__create_credits_menu()
        self.__create_main_menu()

        self.__is_enabled = self.__main_menu.is_enabled()

    def __create_main_menu(self) -> None:
        self.__main_menu: pygame_menu.Menu = pygame_menu.Menu('Main menu', self.__menu_width, self.__menu_height,
                                                              theme=self.__menu_theme, position=MENU_POSITION,
                                                              mouse_motion_selection=True)
        self.__main_menu.add.button('Play', self.__play_menu)
        self.__main_menu.add.button('Options', self.__options_menu)
        self.__main_menu.add.button('Credits', self.__credits)

        self.__main_menu.add.button('Quit', pygame_menu.events.EXIT)
        Menu.set_menu_size(self.__main_menu)
        if self.__main_menu.get_width() < MENU_MIN_WIDTH:
            self.__main_menu.resize(MENU_MIN_WIDTH, self.__main_menu.get_height())

    def __create_options_menu(self) -> None:
        self.__options_menu: pygame_menu.Menu = pygame_menu.Menu('Options', self.__menu_width, self.__menu_height,
                                                                 theme=self.__menu_theme, mouse_motion_selection=True)
        self.__options_menu.add.button('Back', pygame_menu.events.BACK)
        self.__options_menu.add.range_slider('Game speed', default=GAME_SPEED[0], range_values=(0, 1), increment=0.1,
                                             rangeslider_id='game_speed_slider')
        self.__options_menu.add.range_slider('Volume', default=SOUND_VOLUME[0], range_values=(0, 1),
                                             increment=0.1, rangeslider_id='volume_slider')

        Menu.set_menu_size(self.__options_menu)

    def __create_play_menu(self, start_game) -> None:
        self.__play_menu: pygame_menu.Menu = pygame_menu.Menu('Play', self.__menu_width, self.__menu_height,
                                                              theme=self.__menu_theme, onclose=pygame_menu.events.BACK
                                                              , mouse_motion_selection=True)
        # print([(game_type.value, 0) for game_type in GameType])
        self.__play_menu.add.button('Battle!', start_game)
        # (title, number of players(game instances) needed or 0 if it's a local game)
        self.__play_menu.add.selector('Game type', [(game_type.value, 0) for game_type in GameType],
                                      selector_id='game_type', style='fancy', style_fancy_bgcolor=(0, 0, 0, 0))
        self.__play_menu.add.text_input('Nickname: ', default=PLAYER_NAMES[0], textinput_id='nickname', maxchar=10)
        self.__play_menu.add.text_input('Game name: ', default=GAME_NAME[0], textinput_id='game_name', maxchar=10)
        self.__play_menu.add.button('Back', pygame_menu.events.BACK)

        Menu.set_menu_size(self.__play_menu)

    def __create_credits_menu(self) -> None:
        self.__credits: pygame_menu.Menu = pygame_menu.Menu('Credits', self.__menu_width, self.__menu_height,
                                                            theme=self.__menu_theme)
        self.__credits.add.label('Vuk Djordjevic')
        self.__credits.add.label('Ricardo Suarez del Valle')
        self.__credits.add.label('Jovan Milanovic')
        self.__credits.add.button('Back', pygame_menu.events.BACK)
        Menu.set_menu_size(self.__credits)

    def __create_menu_theme(self) -> None:
        self.__menu_theme = pygame_menu.themes.THEME_DARK.copy()
        self.__menu_theme.title = False
        self.__menu_theme.background_color = MENU_BACKGROUND_COLOR
        self.__menu_theme.widget_font = pygame_menu.font.FONT_NEVIS
        self.__menu_theme.selection_color = MENU_SELECTED_TEXT_COLOR
        self.__menu_theme.widget_font_color = WHITE
        self.__menu_theme.widget_alignment = pygame_menu.locals.ALIGN_LEFT
        self.__menu_theme.widget_font = MENU_FONT

    def disable(self) -> None:
        self.__main_menu.disable()

    def enable(self) -> None:
        self.__main_menu.enable()

    def draw(self, screen) -> None:
        if self.__main_menu.is_enabled():
            self.__main_menu.draw(screen)

    def update(self, events: list[pygame.event.Event]) -> None:
        self.__main_menu.update(events)

    def is_enabled(self) -> bool:
        return self.__main_menu.is_enabled()

    def get_volume(self) -> float:
        return self.__options_menu.get_widget('volume_slider').get_value()

    def get_map_name(self) -> str:
        return self.__play_menu.get_widget('game_name').get_value()

    def get_player_name(self) -> str:
        return self.__play_menu.get_widget('nickname').get_value()

    def get_game_type(self) -> int:
        return self.__play_menu.get_widget('game_type').get_value()[0][0]

    def get_game_speed(self) -> float:
        return self.__options_menu.get_widget('game_speed_slider').get_value()

    @staticmethod
    def set_menu_size(menu: pygame_menu.Menu) -> None:
        max_width, height = 1, 1
        for widget in menu.get_widgets():
            max_width = max(max_width, widget.get_width())
            height += widget.get_height()

        menu.resize(max_width, height, position=MENU_POSITION)
