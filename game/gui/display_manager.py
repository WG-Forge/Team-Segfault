import os

from game.constants import FPS_MAX, SCREEN_WIDTH, SCREEN_HEIGHT, MENU_BACKGROUND_IMAGE, GUI_ICON_PATH, \
    GAME_BACKGROUND, TRACKS_IMAGE_PATH
from game.gui.menu import *
from tests.multiplayer_game import multiplayer_game
from tests.single_player_game import single_player_game

os.environ['SDL_VIDEO_CENTERED'] = '1'  # window at center


class DisplayManager:

    def __init__(self):

        super().__init__()
        pygame.init()
        pygame.display.set_icon(pygame.image.load(GUI_ICON_PATH))

        self.__screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        pygame.display.set_caption("Team Segfault")

        self.__running = True
        self.__playing = False

        self.__game = None

        self.__clock = pygame.time.Clock()

        # load images
        self.__background_image = pygame.transform.scale(pygame.image.load(MENU_BACKGROUND_IMAGE),
                                                         (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.__tracks_image = pygame.image.load(TRACKS_IMAGE_PATH)

        # create menu
        self.__menu = Menu(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3, self.__start_the_game)

    def __start_the_game(self) -> None:
        del self.__game
        self.__menu.disable()
        SOUND_VOLUME[0] = self.__menu.get_volume()
        PLAYER_NAMES[0] = self.__menu.get_player_name()
        GAME_NAME[0] = self.__menu.get_map_name()
        game_type = self.__menu.get_game_type()
        match game_type:
            case GameType.SINGLEPLAYER:
                self.__game = single_player_game()
            # case GameType.PVP_MULTIPLAYER:
            #     self.__name = pvp_game()
            case GameType.LOCAL_MULTIPLAYER:
                self.__game = multiplayer_game(GAME_NAME[0], PLAYER_NAMES[0], PLAYER_NAMES[1], PLAYER_NAMES[2])
            # case GameType.SPECTATE:
            #     _ = remote_game_create()
            #     self.__game = remote_game_join()
            case _:
                self.__menu.enable()
                return
        self.__playing = True
        # self.__start_loading_screen()
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

    def __start_loading_screen(self) -> None:
        pass
        # rect = self.__tracks_image.get_rect()
        # start = time.time()
        # start += 1
        # while time.time() < start:
        #     self.__screen.blit(self.__tracks_image, (50, SCREEN_HEIGHT / 2))
        #     # delay for a constant framerate
        #     self.__clock.tick(FPS_MAX)
        #
        #     # update display
        #     pygame.display.flip()

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

            # draw the map if the game started
            if self.__playing and not self.__game.over.is_set() and self.__game.game_map:
                self.__game.game_map.draw(self.__screen)

            # check if game has ended
            if self.__playing and self.__game.over.is_set():
                # EndScreen.draw_podium(self.__screen, {})
                # self.__clock.tick(FPS_MAX)
                # pygame.display.flip()
                self.__menu.enable()

            # delay for a constant framerate
            self.__clock.tick(FPS_MAX)

            # update display
            pygame.display.flip()

    def __draw_background(self) -> None:
        self.__screen.fill(GAME_BACKGROUND)
        self.__screen.blit(self.__background_image, (0, 0))
