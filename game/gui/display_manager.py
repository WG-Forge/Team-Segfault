import os

import pygame
import pygame_menu

from constants import FPS_MAX, SCREEN_WIDTH, SCREEN_HEIGHT, SOUND_VOLUME, PLAYER1_NAME

os.environ['SDL_VIDEO_CENTERED'] = '1'  # window at center


class DisplayManager:

    def __init__(self, game):

        super().__init__()
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        pygame.display.set_caption("Team Segfault")

        self.running = True
        self.playing = False

        self.game = game

        self.__clock = pygame.time.Clock()

        # configure controls window
        self.controls = pygame_menu.Menu('Controls', SCREEN_WIDTH, SCREEN_HEIGHT, theme=pygame_menu.themes.THEME_DARK)
        # self.controls.add.button('')
        self.controls.add.button('Back', pygame_menu.events.BACK)

        # configure credits window
        self.credits = pygame_menu.Menu('Credits', SCREEN_WIDTH, SCREEN_HEIGHT, theme=pygame_menu.themes.THEME_DARK)
        self.credits.add.button('Vuk Djordjevic')
        self.credits.add.button('Ricardo Suarez del Valle')
        self.credits.add.button('Jovan Milanovic')
        self.credits.add.button('Back', pygame_menu.events.BACK)

        # configure main menu screen
        self.menu = pygame_menu.Menu('Tank game', SCREEN_WIDTH, SCREEN_HEIGHT, theme=pygame_menu.themes.THEME_DARK)

        self.menu.add.text_input('Name :', default=PLAYER1_NAME[0], onchange=self.change_name)
        self.menu.add.button('Play', self.start_the_game)
        self.menu.add.range_slider('Volume', 0, (0, 1), increment=0.1, onchange=self.change_volume)
        self.menu.add.button('Controls', self.controls)
        self.menu.add.button('Credits', self.credits)

        self.menu.add.button('Quit', pygame_menu.events.EXIT)

        # configure end game menu
        self.end_game_menu = pygame_menu.Menu('Game finished!', SCREEN_WIDTH, SCREEN_HEIGHT,
                                              theme=pygame_menu.themes.THEME_DARK)
        self.end_game_menu.add.button('Play again', self.play_again)
        self.end_game_menu.add.button('Check stats', self.show_stats)
        self.end_game_menu.add.button('Exit', pygame_menu.events.EXIT)

    def start_the_game(self) -> None:
        self.menu.disable()
        self.playing = True
        self.game.start_game()

    def change_volume(self, value: float) -> None:
        # since the sounds are too loud, (0, 1) is being mapped to (0, 0.5)
        SOUND_VOLUME[0] = value / 2

    def change_name(self, value: str) -> None:
        PLAYER1_NAME[0] = value

    def play_again(self) -> None:
        pass

    def show_stats(self) -> None:
        pass

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # set the game end
                self.game.over.set()
                self.playing = False
                self.running = False

    def run(self) -> None:

        # start menu loop
        self.menu.mainloop(self.screen)

        while self.running:

            while self.playing and not self.game.over.is_set():
                self.check_events()

                # draw the map
                self.game.game_map.draw(self.screen)

                # delay for a constant framerate
                self.__clock.tick(FPS_MAX)

                # update display
                pygame.display.flip()

            # check if game has ended
            if self.game.over.is_set():
                if self.playing:
                    self.end_game_menu.mainloop(self.screen)
                    pass
                break

        # cleanup
        pygame.quit()
