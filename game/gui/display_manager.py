import os

from constants import FPS_MAX, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, MENU_FONT
from gui.menu import *

os.environ['SDL_VIDEO_CENTERED'] = '1'  # window at center


class DisplayManager:

    def __init__(self, game):

        super().__init__()
        pygame.init()

        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

        self.DISPLAY_W = SCREEN_WIDTH
        self.DISPLAY_H = SCREEN_HEIGHT

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.font_name = MENU_FONT

        pygame.display.set_caption("Tank Game")

        self.running = True
        self.playing = False

        # Referencing the main menu object - which won't change
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)

        # This variable will change based on the menu
        self.curr_menu = self.main_menu

        self.game = game

        self.__clock = pygame.time.Clock()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # interrupt the game
                self.game.over.set()

                # set everything else to ended
                self.playing = False
                self.running = False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def run(self) -> None:
        try:
            self.__run()
        finally:
            # ensure cleanup
            self.game.over.set()
            pygame.quit()

    def __run(self):
        while self.running:
            self.curr_menu.display_menu()

            while self.playing and not self.game.over.is_set():
                self.check_events()

                if self.game.game_map:
                    # draw the map if the game started
                    self.game.game_map.draw(self.screen)

                # delay for a constant framerate
                self.__clock.tick(FPS_MAX)

                # update display
                pygame.display.flip()

            if self.playing and self.game.over.is_set():
                # quit from the game if it has ended - potentially draw a victory screen here
                break
