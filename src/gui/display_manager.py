import os

import pygame.draw

from src.constants import FPS_MAX, SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_IMAGE_PATH, GUI_ICON_PATH, \
    GAME_BACKGROUND, GUI_CAPTION, MAP_TYPE, ERROR_FONT_SIZE, ERROR_MESSAGE_COLOR, HEX_RADIUS_Y, ERROR_BUTTON_DIMENSIONS, \
    ERROR_BUTTON_POSITION
from src.game_presets.local_multiplayer import local_multiplayer_game
from src.game_presets.pvp_game import pvp_game
from src.game_presets.single_player import single_player_game
from src.game_presets.spectator import spectator_game
from src.gui.menus_and_screens.end_screen import EndScreen
from src.gui.menus_and_screens.loading_screen import LoadingScreen
from src.gui.menus_and_screens.menu import *

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

        self.__error_happened = False
        self.__mouse_pos: tuple = (-1, -1)

        self.__end_screen: EndScreen = EndScreen()

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
        GAME_NAME[0] = self.__menu.game_name
        GAME_SPEED[0] = self.__menu.game_speed
        ADVANCED_GRAPHICS[0] = self.__menu.advanced_graphics
        MAP_TYPE[0] = self.__menu.map_type
        game_type = self.__menu.game_type

        match game_type:
            case GameType.SINGLE_PLAYER:
                self.__game = single_player_game(GAME_NAME[0], PLAYER_NAMES[0])
            case GameType.PVP_MULTIPLAYER:
                self.__game = pvp_game(GAME_NAME[0], PLAYER_NAMES[0])
            case GameType.LOCAL_MULTIPLAYER:
                self.__game = local_multiplayer_game(game_name=GAME_NAME[0],
                                                     player_names=PLAYER_NAMES[:3],
                                                     is_full=self.__menu.full_game)
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
            if event.type == pygame.MOUSEBUTTONDOWN and self.__error_happened is True and self.__check_mouse_click():
                self.__menu.enable()
                self.__game.over.set()
                self.__game = None
                self.__error_happened = False
                # stop the game -> set the self.__playing flag to False
                self.__playing = False
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
        players = []
        while self.__running:
            self.__mouse_pos = pygame.mouse.get_pos()

            self.__draw_background()
            events = self.__check_events()

            if self.__menu.is_enabled():
                self.__menu.update(events)
                self.__menu.draw(self.__screen)

            # check if error happened
            if self.__game and self.__game.connection_error is not None:
                self.__error_happened = True
                self.__draw_error(self.__game.connection_error)
                self.__menu.disable()

            # draw the map or loading screen if the game started
            if self.__playing and not self.__game.over.is_set():
                players = self.__game.player_wins_and_info
                self.__game.game_map.draw(self.__screen) if self.__game.game_map \
                    else self.__loading_screen.draw(self.__screen)

            # check if game has ended
            if self.__playing and self.__game.over.is_set():
                self.__loading_screen.reset()
                self.__playing = False
                # self.__end_screen.toggle_enable()  # uncomment this and comment the line below for podium display
                self.__menu.enable()

            if self.__end_screen and self.__end_screen.enabled:
                # delete shadow client and sort the list
                players = sorted(filter(lambda x: x[1] is not None, self.__game.player_wins_and_info),
                                 key=lambda x: x[0], reverse=True)
                self.__end_screen.draw_podium(self.__screen, players)

            # delay for a constant framerate
            self.__clock.tick(FPS_MAX)

            # update display
            pygame.display.flip()

    def __draw_background(self) -> None:
        self.__screen.fill(GAME_BACKGROUND)
        self.__screen.blit(self.__background_image, (0, 0))

    def __draw_error(self, text) -> None:
        # display text
        error_number, error_msg = str(text).split(':')
        error_number = pygame.font.Font(MENU_FONT, ERROR_FONT_SIZE).render(error_number, True, ERROR_MESSAGE_COLOR)
        error_msg = pygame.font.Font(MENU_FONT, ERROR_FONT_SIZE).render(error_msg, True, ERROR_MESSAGE_COLOR)
        self.__screen.blit(error_number, ((SCREEN_WIDTH - error_number.get_width()) / 2, HEX_RADIUS_Y[0]))
        self.__screen.blit(error_msg, ((SCREEN_WIDTH - error_msg.get_width()) / 2,
                                       HEX_RADIUS_Y[0] + error_number.get_height()))

        # show button
        pygame.draw.rect(self.__screen, ERROR_MESSAGE_COLOR, (ERROR_BUTTON_POSITION[0], ERROR_BUTTON_POSITION[1],
                                                              ERROR_BUTTON_DIMENSIONS[0], ERROR_BUTTON_DIMENSIONS[1]))
        btn_text = pygame.font.Font(MENU_FONT, ERROR_FONT_SIZE).render('Menu', True, 'white')
        btn_rect = btn_text.get_rect(center=(ERROR_BUTTON_POSITION[0] + ERROR_BUTTON_DIMENSIONS[0] // 2,
                                             ERROR_BUTTON_POSITION[1] + ERROR_BUTTON_DIMENSIONS[1] // 2))
        self.__screen.blit(btn_text, btn_rect)

    def __check_mouse_click(self) -> bool:
        return ERROR_BUTTON_POSITION[0] + ERROR_BUTTON_DIMENSIONS[0] > \
               self.__mouse_pos[0] > ERROR_BUTTON_POSITION[0] and \
               ERROR_BUTTON_POSITION[1] + ERROR_BUTTON_DIMENSIONS[1] > \
               self.__mouse_pos[1] > ERROR_BUTTON_POSITION[1]
