import os

import pygame
import pygame_menu

from constants import FPS_MAX, SCREEN_WIDTH, SCREEN_HEIGHT, SOUND_VOLUME, PLAYER1_NAME, MENU_IMAGE

os.environ['SDL_VIDEO_CENTERED'] = '1'  # window at center


class DisplayManager:

    def __init__(self, game):

        super().__init__()
        pygame.init()

        self.__screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        pygame.display.set_caption("Team Segfault")

        self.__running = True
        self.__playing = False

        self.__game = game

        self.__clock = pygame.time.Clock()

        # configure controls window
        self.__controls = pygame_menu.Menu('Controls', SCREEN_WIDTH, SCREEN_HEIGHT, theme=pygame_menu.themes.THEME_DARK)
        # self.__controls.add.button('')
        self.__controls.add.button('Back', pygame_menu.events.BACK)

        # configure credits window
        self.__credits = pygame_menu.Menu('Credits', SCREEN_WIDTH, SCREEN_HEIGHT, theme=pygame_menu.themes.THEME_DARK)
        self.__credits.add.button('Vuk Djordjevic')
        self.__credits.add.button('Ricardo Suarez del Valle')
        self.__credits.add.button('Jovan Milanovic')
        self.__credits.add.button('Back', pygame_menu.events.BACK)

        # todo find better image
        menu_theme = pygame_menu.themes.THEME_DARK.copy()
        image = pygame_menu.baseimage.BaseImage(
            image_path=MENU_IMAGE,
            drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY
        )
        menu_theme.background_color = image

        # configure main menu screen
        self.__menu = pygame_menu.Menu('Tank game', SCREEN_WIDTH, SCREEN_HEIGHT, theme=menu_theme)

        self.__menu.add.text_input('Name :', default=PLAYER1_NAME[0], onchange=self.__change_name)
        self.__menu.add.button('Play', self.__start_the_game)
        self.__menu.add.range_slider('Volume', 0, (0, 1), increment=0.1, onchange=self.__change_volume)
        self.__menu.add.button('Controls', self.__controls)
        self.__menu.add.button('Credits', self.__credits)

        self.__menu.add.button('Quit', pygame_menu.events.EXIT)

        # configure end game menu
        self.__end_game_menu = pygame_menu.Menu('Game finished!', SCREEN_WIDTH, SCREEN_HEIGHT,
                                                theme=pygame_menu.themes.THEME_DARK)
        self.__end_game_menu.add.button('Play again', self.__play_again)
        self.__end_game_menu.add.button('Check stats', self.__show_stats)
        self.__end_game_menu.add.button('Exit', pygame_menu.events.EXIT)

    def __start_the_game(self) -> None:
        self.__menu.disable()
        self.__playing = True
        self.__game.start_game()

    def __change_volume(self, value: float) -> None:
        # since the sounds are too loud, (0, 1) is being mapped to (0, 0.5)
        SOUND_VOLUME[0] = value / 2

    def __change_name(self, value: str) -> None:
        PLAYER1_NAME[0] = value

    def __play_again(self) -> None:
        pass

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
        self.__menu.mainloop(self.__screen)

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
                break

        # cleanup
        pygame.quit()
