import pygame

from constants import BLACK


class Menu:
    def __init__(self, display_manager):
        self.display_manager = display_manager
        self.mid_w, self.mid_h = self.display_manager.DISPLAY_W / 2, self.display_manager.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100

    def draw_cursor(self):
        self.display_manager.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        pygame.display.flip()
        self.display_manager.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"

        # todo: remove magic numbers with font scaling or screen size
        self.states = ("Start", "Options", "Help", "Credits", "Exit")
        self.state_sz = len(self.states)
        self.state_ind = 0
        self.statex = tuple([self.mid_w for _ in range(self.state_sz)])
        self.statey = tuple([self.mid_h + 30 + 20 * i for i in range(self.state_sz)])
        self.cursor_rect.midtop = (self.statex[self.state_ind] + self.offset, self.statey[self.state_ind])

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.display_manager.check_events()
            self.check_input()
            self.display_manager.screen.fill(BLACK)
            self.display_manager.draw_text('Main Menu', 20, self.display_manager.DISPLAY_W / 2,
                                           self.display_manager.DISPLAY_H / 2 - 20)
            for i in range(self.state_sz):
                self.display_manager.draw_text(self.states[i], 20, self.statex[i], self.statey[i])
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        # scrolling up and down - keyboard controls
        if self.display_manager.DOWN_KEY:
            self.state_ind = (self.state_ind + 1) % self.state_sz
            self.state = self.states[self.state_ind]
            self.cursor_rect.midtop = (self.statex[self.state_ind] + self.offset, self.statey[self.state_ind])
        elif self.display_manager.UP_KEY:
            self.state_ind = (self.state_ind - 1) % self.state_sz
            self.state = self.states[self.state_ind]
            self.cursor_rect.midtop = (self.statex[self.state_ind] + self.offset, self.statey[self.state_ind])

    def check_input(self):
        # are some of the menues selected?
        self.move_cursor()
        if self.display_manager.START_KEY:
            if self.state == 'Start':
                self.display_manager.playing = True
                self.display_manager.game.start_game()
            elif self.state == 'Options':
                self.display_manager.curr_menu = self.display_manager.options
            elif self.state == 'Credits':
                self.display_manager.curr_menu = self.display_manager.credits
            self.run_display = False


class OptionsMenu(Menu):
    def __init__(self, display_manager):
        Menu.__init__(self, display_manager)
        self.state = 'Volume'
        self.volx, self.voly = self.mid_w, self.mid_h + 20
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 40
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.display_manager.check_events()
            self.check_input()
            self.display_manager.screen.fill(BLACK)
            self.display_manager.draw_text('Options', 20, self.display_manager.DISPLAY_W / 2,
                                           self.display_manager.DISPLAY_H / 2 - 30)
            self.display_manager.draw_text("Volume", 15, self.volx, self.voly)
            self.display_manager.draw_text("Controls", 15, self.controlsx, self.controlsy)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.display_manager.BACK_KEY:
            self.display_manager.curr_menu = self.display_manager.main_menu
            self.run_display = False
        elif self.display_manager.UP_KEY or self.display_manager.DOWN_KEY:
            if self.state == 'Volume':
                self.state = 'Controls'
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
            elif self.state == 'Controls':
                self.state = 'Volume'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        elif self.display_manager.START_KEY:
            # TODO
            pass


class CreditsMenu(Menu):
    def __init__(self, display_manager):
        Menu.__init__(self, display_manager)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.display_manager.check_events()
            if self.display_manager.START_KEY or self.display_manager.BACK_KEY:
                self.display_manager.curr_menu = self.display_manager.main_menu
                self.run_display = False
            self.display_manager.screen.fill(BLACK)
            self.display_manager.draw_text('Credits', 20, self.display_manager.DISPLAY_W / 2,
                                           self.display_manager.DISPLAY_H / 2 - 20)
            self.display_manager.draw_text('Jovan Milanovic', 15, self.display_manager.DISPLAY_W / 2,
                                           self.display_manager.DISPLAY_H / 2 + 10)
            self.display_manager.draw_text('Ricardo Suarez del Valle', 15, self.display_manager.DISPLAY_W / 2,
                                           self.display_manager.DISPLAY_H / 2 + 30)
            self.display_manager.draw_text('Vuk Djordjevic', 15, self.display_manager.DISPLAY_W / 2,
                                           self.display_manager.DISPLAY_H / 2 + 50)
            self.blit_screen()
