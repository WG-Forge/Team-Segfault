import pygame
from pygame import Surface
from pygame.sprite import Sprite

from constants import SCREEN_WIDTH, GAME_BACKGROUND, HEX_RADIUS_X, HEX_RADIUS_Y
from entity.map_features.base import Base
from entity.map_features.empty import Empty
from entity.map_features.obstacle import Obstacle
from entity.tanks.tank import Tank
from gui.map_utils.explosion import Explosion
from gui.map_utils.projectile import Projectile
from gui.map_utils.scoreboard import Scoreboard
from gui.map_utils.tank_drawer import TankDrawer
from map.hex import Hex


class MapDrawer:
    def __init__(self, map_size: int, players: dict, game_map: dict, current_turn: list[1]):
        self.__map_size = map_size
        self.__turn: list[1] = current_turn
        self.__max_damage_points: int = 0
        self.__players = players
        self.__map = game_map

        Explosion.set_image_scale()
        self.__scoreboard = Scoreboard(players)
        # self.__scoreboard.update_image_size(HEX_RADIUS_X[0] * 2, HEX_RADIUS_Y[0] * 2)
        self.__font_size = round(1.2 * min(HEX_RADIUS_X[0], HEX_RADIUS_Y[0]))
        self.__font = None
        self.__explosion_group = pygame.sprite.Group()
        self.__projectile_group = pygame.sprite.Group()
        # note: this could be moved somewhere else
        self.__explosion_delay = Projectile.get_travel_time()

        # map legend
        self.__map_legend_items = []
        features = [Empty, Base, Obstacle]
        # this will always be on the screen and on top right
        x, y, z = self.__map_size + 1, self.__map_size - 2, -self.__map_size - 1
        for i, feature in enumerate(features):
            self.__map_legend_items.append(feature((x, y - i, z + i)))

        # tanks
        self.__tanks = pygame.sprite.Group()
        for _, entities in self.__map.items():
            tank = entities['tank']
            if tank is not None:
                self.__tanks.add(TankDrawer(tank))

    def draw(self, screen: Surface):
        if self.__font is None:
            self.__font = pygame.font.SysFont('georgia', self.__font_size, bold=True)

        # fill with background color
        screen.fill(GAME_BACKGROUND)

        # display tanks and features
        for coord, entities in self.__map.items():
            feature, tank = entities['feature'], entities['tank']
            self.draw_feature(screen, feature)

        # draw tanks
        self.__tanks.draw(screen)
        self.__tanks.update(screen)

        # display scoreboards
        self.__scoreboard.draw_damage_scoreboard(screen, self.__font, self.__font_size, self.__max_damage_points)
        self.__scoreboard.draw_capture_scoreboard(screen, self.__font, self.__font_size)

        # draw explosions
        self.__explosion_group.draw(screen)
        self.__explosion_group.update()

        # draw projectiles
        self.__projectile_group.draw(screen)
        self.__projectile_group.update()

        # display turn
        if self.__turn is not None:
            text = self.__font.render('Turn: ' + str(self.__turn[0]), True, 'grey')
            text_rect = text.get_rect(midtop=(SCREEN_WIDTH // 2, 0))
            screen.blit(text, text_rect)

        # draw map legend
        self.draw_legend(screen)

        pygame.display.flip()

    def draw_feature(self, screen, feature):
        """Renders the hexagon on the screen and draw a white border around the hexagon"""
        pygame.draw.polygon(screen, feature.get_color(), feature.get_corners())
        pygame.draw.aalines(screen, (255, 255, 255), closed=True, points=feature.get_corners())

    def draw_legend(self, screen: Surface):
        y = 0
        for feature in self.__map_legend_items:
            text = self.__font.render(' ' + str(feature.type), True, 'grey')
            text_rect = text.get_rect(midleft=(feature.get_center()[0] + HEX_RADIUS_X[0], feature.get_center()[1]))
            screen.blit(text, text_rect)
            y += 2 * HEX_RADIUS_Y[0]
            self.draw_feature(screen, feature)

    """Adding sprites to their group"""

    def add_explosion(self, tank: Tank, target: Tank) -> None:
        self.__max_damage_points = \
            max(self.__max_damage_points, self.__players[tank.get_player_index()].get_damage_points())

        explosion: Sprite = Explosion(Hex.make_center(target.get_coord()))
        self.__explosion_group.add(explosion)

    def add_shot(self, start_pos: (), end_pos: (), color):
        projectile: Sprite = Projectile(start_pos, end_pos, color)
        self.__projectile_group.add(projectile)
