import os

import pygame
import pygame_menu

from constants import FPS_MAX, SCREEN_WIDTH, SCREEN_HEIGHT, SOUND_VOLUME, MENU_IMAGE, MENU_TEXT_COLOR, \
    MENU_SELECTED_TEXT_COLOR, PLAYER_NAMES, GAME_NAME
from tests.multiplayer_game import multiplayer_game
from tests.single_player_game import single_player_game

os.environ['SDL_VIDEO_CENTERED'] = '1'  # window at center


class DisplayManager:

    def __init__(self):

        super().__init__()
        pygame.init()

        self.__screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        pygame.display.set_caption("Team Segfault")

        self.__running = True
        self.__playing = False

        self.__game = None

        self.__clock = pygame.time.Clock()

        # create theme
        self.__create_menu_theme()

        # submenus need to be created before main menu
        self.__create_play_menu()
        self.__create_controls_menu()
        self.__create_credits_menu()
        self.__create_main_menu()
        self.__create_end_game_menu()

    def __start_the_game(self) -> None:
        del self.__game
        self.__play_menu.close()
        self.__main_menu.disable()
        SOUND_VOLUME[0] = self.__main_menu.get_widget('volume_slider').get_value()
        PLAYER_NAMES[0] = self.__play_menu.get_widget('nickname').get_value()
        GAME_NAME[0] = self.__play_menu.get_widget('game_name').get_value()
        players = self.__play_menu.get_widget('game_type').get_value()[0][1]
        if players == 0:
            self.__game = single_player_game()
        elif players == 3:
            self.__game = multiplayer_game(GAME_NAME[0], PLAYER_NAMES[0], PLAYER_NAMES[1], PLAYER_NAMES[2])
        else:
            self.__main_menu.enable()
            return
        self.__playing = True
        self.__game.start()

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
        try:
            self.__run()
        finally:
            # ensure cleanup
            self.__game.over.set()
            pygame.quit()

    def __run(self) -> None:
        # start menu loop
        self.__main_menu.enable()
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
            if self.__game.over.is_set() and self.__playing:
                self.__main_menu.enable()
                self.__end_game_menu.enable()
                self.__end_game_menu.mainloop(self.__screen)

    def __create_main_menu(self) -> None:
        self.__main_menu = pygame_menu.Menu('Tank game', SCREEN_WIDTH, SCREEN_HEIGHT, theme=self.__menu_theme)
        self.__main_menu.add.button('Play', self.__play_menu)
        self.__main_menu.add.range_slider('Volume', default=SOUND_VOLUME[0], range_values=(0, 1),
                                          increment=0.1, rangeslider_id='volume_slider')
        self.__main_menu.add.button('Controls', self.__controls)
        self.__main_menu.add.button('Credits', self.__credits)

        self.__main_menu.add.button('Quit', pygame_menu.events.EXIT)

    def __create_play_menu(self) -> None:
        self.__play_menu = pygame_menu.Menu('Play', SCREEN_WIDTH, SCREEN_HEIGHT, theme=self.__menu_theme,
                                            onclose=pygame_menu.events.BACK)
        self.__play_menu.add.button('Start the game', self.__start_the_game)
        # (title, number of players(game instances) needed or 0 if it's a local game)
        self.__play_menu.add.selector('Game type', [('Multiplayer game simulation', 3),
                                                    ('Multiplayer game against other players', 1),
                                                    ('Local solo game', 0),
                                                    ('Spectating game', 4)], selector_id='game_type')
        self.__play_menu.add.text_input('Nickname :', default=PLAYER_NAMES[0], textinput_id='nickname')
        self.__play_menu.add.text_input('Game name:', default=GAME_NAME[0], textinput_id='game_name')
        self.__play_menu.add.button('Back', pygame_menu.events.BACK)

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
        self.__end_game_menu.add.button('Play again', self.__main_menu)
        self.__end_game_menu.add.button('Check stats', self.__show_stats)
        self.__end_game_menu.add.button('Exit', pygame_menu.events.EXIT)

    def __create_menu_theme(self) -> None:
        # todo find better colors; place menu options at bottom left
        self.__menu_theme = pygame_menu.themes.THEME_DARK.copy()
        image = pygame_menu.baseimage.BaseImage(
            image_path=MENU_IMAGE,
            drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL
        )
        self.__menu_theme.background_color = image
        self.__menu_theme.widget_font = pygame_menu.font.FONT_NEVIS
        self.__menu_theme.selection_color = MENU_SELECTED_TEXT_COLOR
        self.__menu_theme.widget_font_color = MENU_TEXT_COLOR
        # self.__menu_theme.widget_alignment = pygame_menu.locals.ALIGN_LEFT
