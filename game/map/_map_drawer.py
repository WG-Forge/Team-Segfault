import pygame
from pygame import Surface
from pygame.sprite import Sprite

from consts import SCREEN_WIDTH, SCREEN_HEIGHT
from entity.tanks.tank import Tank
from map.hex import Hex
from pygame_utils.explosion import Explosion
from pygame_utils.scoreboard import Scoreboard


class MapDrawer:
    def __init__(self, map_size: int, players: tuple, game_map: dict, current_turn: list[1]):
        self.__scoreboard = Scoreboard(players)
        self.__num_of_radii = (map_size - 1) * 2 * 2

        Hex.radius_x = SCREEN_WIDTH // self.__num_of_radii  # number of half radii on x axis
        Hex.radius_y = SCREEN_HEIGHT // self.__num_of_radii  # number of half radii on y axis

        self.__scoreboard.update_image_size(Hex.radius_x * 2, Hex.radius_y * 2)
        self.__scoreboard.set_radii(Hex.radius_x / 3, Hex.radius_y / 3)
        self.__font_size = round(1.2 * min(Hex.radius_y, Hex.radius_x))
        self.__explosion_group = pygame.sprite.Group()
        self.__turn: list[1] = current_turn
        self.__max_damage_points: int = 0
        self.__players = players

        self.__map = game_map

    def draw(self, screen: Surface):
        # Pass the surface and use it for rendering
        font = pygame.font.SysFont('georgia', self.__font_size, bold=True)
        # fill with background color
        screen.fill((59, 56, 47))

        # display tanks and features
        for coord, entities in self.__map.items():
            feature, tank = entities['feature'], entities['tank']
            feature.draw(screen)
            # Draw tank if any
            if tank is not None:
                tank.draw(screen, self.__font_size)

        # display scoreboards
        self.__scoreboard.draw_damage_scoreboard(screen, font, self.__font_size, self.__max_damage_points)
        self.__scoreboard.draw_capture_scoreboard(screen, font, self.__font_size)

        self.__explosion_group.draw(screen)
        self.__explosion_group.update()

        # display turn
        if self.__turn is not None:
            text = font.render('Turn: ' + str(self.__turn[0]), True, 'grey')
            text_rect = text.get_rect(midtop=(screen.get_width() // 2, 0))
            screen.blit(text, text_rect)

        pygame.display.flip()

    def add_explosion(self, tank: Tank, target: Tank):
        explosion: Sprite = Explosion(target.get_screen_position(), Hex.radius_x * 2, Hex.radius_y * 2)
        self.__explosion_group.add(explosion)

        self.__max_damage_points = \
            max(self.__max_damage_points, self.__players[tank.get_player_index()].get_damage_points())
