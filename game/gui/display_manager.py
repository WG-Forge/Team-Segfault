import os
import random

import pygame
import pygame_menu

from constants import FPS_MAX, SCREEN_WIDTH, SCREEN_HEIGHT, SOUND_VOLUME, PLAYER_NAMES, MENU_IMAGE, MENU_TEXT_COLOR, \
    MENU_SELECTED_TEXT_COLOR, GAME_NAME
from game.game import Game

os.environ['SDL_VIDEO_CENTERED'] = '1'  # window at center


class DisplayManager:

    def __init__(self):

        super().__init__()
        pygame.init()

        self.__screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        pygame.display.set_caption("Team Segfault")

        self.__running = True
        self.__playing = False

        self.__game: Game | None = None

        self.__clock = pygame.time.Clock()

        # create theme
        self.__create_menu_theme()

        # submenus need to be created before main menu
        self.__create_controls_menu()
        self.__create_credits_menu()
        self.__create_main_menu()
        self.__create_end_game_menu()

    def __start_the_game(self) -> None:
        self.__main_menu.disable()
        self.__playing = True
        # create a game according to chosen settings (for now its only 1 player + 2 bots, 3 instances total)
        name: str = "Test game 1: "
        name += str(random.randint(0, 10000))
        self.__game = Game(game_name=name, max_players=3, num_turns=45)
        self.__game.add_local_player(name=PLAYER_NAMES[0], is_observer=False)
        self.__game.add_local_player(name="Blue bot", is_observer=False)
        self.__game.add_local_player(name="Red bot", is_observer=False)

        self.__game.start_game()

    def __change_volume(self, value: float) -> None:
        # since the sounds are too loud, (0, 1) is being mapped to (0, 0.5)
        SOUND_VOLUME[0] = value / 2

    def __change_name(self, value: str) -> None:
        PLAYER_NAMES[0] = value

    def __play_again(self) -> None:
        # todo
        self.__end_game_menu.disable()
        self.__start_the_game()

    def __show_stats(self) -> None:
        pass

    def __check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # set the game end
                self.__game.over.set()
                self.__playing = False
                self.__running = False

    def run(self) -> None:

        # start menu loop
        self.__main_menu.mainloop(self.__screen)

        while self.__running:

            while self.__playing and not self.__game.over.is_set():
                self.__check_events()

                if self.__game.game_map:
                    # draw the map if the game started
                    self.__game.game_map.draw(self.__screen)

                # delay for a constant framerate
                self.__clock.tick(FPS_MAX)

                # update display
                pygame.display.flip()

            # check if game has ended
            if self.__game.over.is_set():
                if self.__playing:
                    self.__end_game_menu.mainloop(self.__screen)
                    pass

        # cleanup
        pygame.quit()

    def __create_main_menu(self) -> None:
        self.__main_menu = pygame_menu.Menu('Tank game', SCREEN_WIDTH, SCREEN_HEIGHT, theme=self.__menu_theme)

        self.__main_menu.add.button('Play', self.__start_the_game)
        self.__main_menu.add.selector('Game type', [('Multiplayer game simulation', 0),
                                                    ('Multiplayer game against other players', 1),
                                                    ('Solo (nameless) game', 2),
                                                    ('Spectating game', 3)], default=0)
        self.__main_menu.add.text_input('Nickname :', default=PLAYER_NAMES[0], onchange=self.__change_name)
        self.__main_menu.add.text_input('Game name:', default=GAME_NAME[0], onchange=self.__change_name)
        self.__main_menu.add.range_slider('Volume', 0, (0, 1), increment=0.1, onchange=self.__change_volume)
        self.__main_menu.add.button('Controls', self.__controls)
        self.__main_menu.add.button('Credits', self.__credits)

        self.__main_menu.add.button('Quit', pygame_menu.events.EXIT)

    def __create_credits_menu(self) -> None:
        self.__credits = pygame_menu.Menu('Credits', SCREEN_WIDTH, SCREEN_HEIGHT, theme=self.__menu_theme)
        self.__credits.add.label('Vuk Djordjevic')
        self.__credits.add.label('Ricardo Suarez del Valle')
        self.__credits.add.label('Jovan Milanovic')
        self.__credits.add.button('Back', pygame_menu.events.BACK)

    def __create_controls_menu(self) -> None:
        self.__controls = pygame_menu.Menu('Controls', SCREEN_WIDTH, SCREEN_HEIGHT, theme=self.__menu_theme)
        # self.__controls.add.button('')
        self.__controls.add.button('Back', pygame_menu.events.BACK)

    def __create_end_game_menu(self) -> None:
        self.__end_game_menu = pygame_menu.Menu('Game finished!', SCREEN_WIDTH, SCREEN_HEIGHT,
                                                theme=self.__menu_theme)
        self.__end_game_menu.add.button('Play again', self.__play_again)
        self.__end_game_menu.add.button('Check stats', self.__show_stats)
        self.__end_game_menu.add.button('Exit', pygame_menu.events.EXIT)

    def __create_menu_theme(self) -> None:
        # todo find better colors (and image maybe)
        self.__menu_theme = pygame_menu.themes.THEME_DARK.copy()
        image = pygame_menu.baseimage.BaseImage(
            image_path=MENU_IMAGE,
            drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL
        )
        self.__menu_theme.background_color = image
        self.__menu_theme.widget_font = pygame_menu.font.FONT_NEVIS
        self.__menu_theme.selection_color = MENU_SELECTED_TEXT_COLOR
        self.__menu_theme.widget_font_color = MENU_TEXT_COLOR
