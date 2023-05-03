import os

from constants import FPS_MAX, SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_IMAGE_PATH, GUI_ICON_PATH, \
    GAME_BACKGROUND, GUI_CAPTION
from game_presets.local_multiplayer import local_multiplayer_game
from game_presets.single_player import single_player_game
from game_presets.spectator import spectator_game
from gui.menus_and_screens.loading_screen import LoadingScreen
from gui.menus_and_screens.menu import *

os.environ['SDL_VIDEO_CENTERED'] = '1'  # window at center


class DisplayManager:

    def __init__(self, game=None):
        pygame.init()
        pygame.display.set_icon(pygame.image.load(GUI_ICON_PATH))

        self.__screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        pygame.display.set_caption(GUI_CAPTION)

        self.__running = True
        self.__playing = False

        self.__game = game

        self.__clock = pygame.time.Clock()

        # load images
        self.__background_image = pygame.transform.scale(pygame.image.load(BACKGROUND_IMAGE_PATH),
                                                         (SCREEN_WIDTH, SCREEN_HEIGHT))

        # create menu
        self.__menu = Menu(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3, self.__start_the_game)

        self.__loading_screen = LoadingScreen()

        if game:
            # I added this part - useful for supporting the tests we already have
            self.__menu.disable()
            self.__playing = True
            self.__game.start()

    def __start_the_game(self) -> None:
        del self.__game
        self.__menu.disable()
        SOUND_VOLUME[0] = self.__menu.volume
        PLAYER_NAMES[0] = self.__menu.player_name
        GAME_NAME[0] = self.__menu.map_name
        GAME_SPEED[0] = self.__menu.game_speed
        ADVANCED_GRAPHICS[0] = self.__menu.advanced_graphics
        print(ADVANCED_GRAPHICS[0])
        game_type = self.__menu.game_type
        match game_type:
            case GameType.SINGLE_PLAYER:
                self.__game = single_player_game(GAME_NAME[0], PLAYER_NAMES[0])
            # case GameType.PVP_MULTIPLAYER:
            #     self.__name = pvp_game()
            case GameType.LOCAL_MULTIPLAYER:
                self.__game = local_multiplayer_game(GAME_NAME[0], PLAYER_NAMES[0], PLAYER_NAMES[1], PLAYER_NAMES[2])
            case GameType.SPECTATE:
                self.__game = spectator_game(GAME_NAME[0], PLAYER_NAMES[1])
            case _:
                self.__menu.enable()
                return
        self.__playing = True
        self.__game.start()

    def __check_events(self) -> list[pygame.event.Event]:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # set the game end
                if self.__game:
                    self.__game.over.set()
                self.__playing = False
                self.__running = False
        return events

    def run(self) -> None:
        try:
            self.__run()
        finally:
            # ensure cleanup
            if self.__game:
                self.__game.over.set()
            pygame.quit()

    def __run(self) -> None:
        while self.__running:
            self.__draw_background()
            events = self.__check_events()

            if self.__menu.is_enabled():
                self.__menu.update(events)
                self.__menu.draw(self.__screen)

            # draw the map or loading screen if the game started
            if self.__playing and not self.__game.over.is_set():
                if self.__game.game_map:
                    self.__game.game_map.draw(self.__screen)
                else:
                    self.__loading_screen.draw(self.__screen)

            # check if game has ended
            if self.__playing and self.__game.over.is_set():
                self.__loading_screen.reset()
                self.__playing = False
                self.__menu.enable()

            # draw end screen if
            # if self.__end_screen.enabled:
            #     self.__end_screen.draw()

            # delay for a constant framerate
            self.__clock.tick(FPS_MAX)

            # update display
            pygame.display.flip()

    def __draw_background(self) -> None:
        self.__screen.fill(GAME_BACKGROUND)
        self.__screen.blit(self.__background_image, (0, 0))
