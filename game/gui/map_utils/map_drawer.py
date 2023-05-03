import queue

import pygame
from pygame import Surface
from pygame.font import Font
from pygame.sprite import Sprite, Group

from constants import SCREEN_WIDTH, HEX_RADIUS_X, HEX_RADIUS_Y, HARD_REPAIR_IMAGE_PATH, LIGHT_REPAIR_IMAGE_PATH, \
    CATAPULT_IMAGE_PATH, WHITE, MENU_FONT, TANK_IMAGE_SCALE, MAP_FONT_SIZE_MULTIPLIER, \
    EMPTY_HEX_GRASS_IMAGE_PATH, HEX_TILE_IMAGES_SCALE, OBSTACLE_HEX_OBSTACLE_IMAGE_PATH, ADVANCED_GRAPHICS
from entities.map_features.bonuses.catapult import Catapult
from entities.map_features.bonuses.hard_repair import HardRepair
from entities.map_features.bonuses.light_repair import LightRepair
from entities.map_features.landmarks.base import Base, Entities, Feature
from entities.map_features.landmarks.empty import Empty
from entities.map_features.landmarks.obstacle import Obstacle
from entities.tanks.tank import Tank
from game_map.hex import Hex
from gui.map_utils.explosion import Explosion
from gui.map_utils.projectile import Projectile
from gui.map_utils.scoreboard import Scoreboard
from gui.map_utils.shot_tank import ShotTank
from gui.map_utils.tank_drawer import TankDrawer


class MapDrawer:
    def __init__(self, map_size: int, players: dict, game_map: dict, current_turn: list[int]):

        self.__map_size = map_size
        self.__turn: list[int] = current_turn
        self.__max_damage_points: int = 0
        self.__players = players
        self.__map = game_map

        Explosion.set_image_scale()
        self.__scoreboard = Scoreboard(players)
        self.__font_size = round(MAP_FONT_SIZE_MULTIPLIER * min(HEX_RADIUS_X[0], HEX_RADIUS_Y[0]))
        self.__font: Font | None = None
        self.__explosion_group: Group = Group()
        self.__projectile_group: Group = Group()
        # tanks that are shot, but not destroyed
        self.__shot_tanks_group: Group = Group()
        # self.__explosion_delay: int = Projectile.get_travel_time()

        # buffered sprite creation - thread-safe queue object
        self.__explosion_group_buf: queue = queue.Queue()
        self.__projectile_group_buf: queue = queue.Queue()
        self.__shot_tanks_group_buf: queue = queue.Queue()

        # map legend
        self.__map_legend_items: list[Feature] = []
        features = [Empty, Base, Obstacle]
        # regular hexes will always be on the screen and on top right, while bonuses will be on bottom right
        x, y, z = self.__map_size, self.__map_size - 1, -self.__map_size - 1
        for i, feature in enumerate(features):
            self.__map_legend_items.append(feature((x, y - i, z + i)))

        x, y, z = self.__map_size + 2, -self.__map_size + 2, self.__map_size
        bonuses = [Catapult, LightRepair, HardRepair]
        for i, bonus in enumerate(bonuses):
            self.__map_legend_items.append(bonus((x, y + i, z - i)))

        # tanks
        self.__tanks: Group = Group()
        for _, entities in self.__map.items():
            tank = entities['tank']
            if tank is not None:
                self.__tanks.add(TankDrawer(tank))

        self.__load_images()

    def draw(self, screen: Surface) -> None:
        if self.__font is None:
            self.__font = pygame.font.Font(MENU_FONT, self.__font_size)

        # display tanks and features
        for coord, entities in self.__map.items():
            feature, tank = entities['feature'], entities['tank']
            self.__draw_feature(screen, feature, tank is not None)

        # create sprites form buffered data
        self.__add_sprites()

        if ADVANCED_GRAPHICS[0]:
            # draw tanks outlines for tanks that have been hit
            self.__shot_tanks_group.draw(screen)
            self.__shot_tanks_group.update()

        # draw tanks
        self.__tanks.draw(screen)
        self.__tanks.update(screen)

        # display scoreboards
        self.__scoreboard.draw_damage_scoreboard(screen, self.__font, self.__font_size, self.__max_damage_points)
        self.__scoreboard.draw_capture_scoreboard(screen, self.__font, self.__font_size)

        if ADVANCED_GRAPHICS[0]:
            # draw explosions
            self.__explosion_group.draw(screen)
            self.__explosion_group.update()

            # draw projectiles
            self.__projectile_group.draw(screen)
            self.__projectile_group.update()

        # display turn
        if self.__turn is not None:
            text = self.__font.render('Turn: ' + str(self.__turn[0]), True, WHITE)
            text_rect = text.get_rect(midtop=(SCREEN_WIDTH // 2, 0))
            screen.blit(text, text_rect)

        # draw map legend
        self.__draw_legend(screen)

    def __add_sprites(self) -> None:
        # add tank shadows
        while not self.__shot_tanks_group_buf.empty():
            coords, image_path, color = self.__shot_tanks_group_buf.get()
            tank: Sprite = ShotTank(coords, image_path, color)
            self.__shot_tanks_group.add(tank)

        # add explosions
        while not self.__explosion_group_buf.empty():
            coord = self.__explosion_group_buf.get()
            explosion: Sprite = Explosion(Hex.make_center(coord))
            self.__explosion_group.add(explosion)

        # add projectiles
        while not self.__projectile_group_buf.empty():
            start_pos, end_pos, color = self.__projectile_group_buf.get()
            projectile: Sprite = Projectile(start_pos, end_pos, color)
            self.__projectile_group.add(projectile)

    def __load_images(self) -> None:
        """Loads all necessary feature images"""
        scale_size = (HEX_RADIUS_X[0] * TANK_IMAGE_SCALE, HEX_RADIUS_Y[0] * TANK_IMAGE_SCALE)
        self.__hard_repair_image = pygame.transform.scale(pygame.image.load(HARD_REPAIR_IMAGE_PATH), scale_size)
        self.__light_repair_image = pygame.transform.scale(pygame.image.load(LIGHT_REPAIR_IMAGE_PATH), scale_size)
        self.__catapult_image = pygame.transform.scale(pygame.image.load(CATAPULT_IMAGE_PATH), scale_size)
        self.__empty_image = pygame.transform.scale(pygame.image.load(EMPTY_HEX_GRASS_IMAGE_PATH),
                                                    (HEX_RADIUS_X[0] * HEX_TILE_IMAGES_SCALE[0],
                                                     HEX_RADIUS_Y[0] * HEX_TILE_IMAGES_SCALE[1]))
        self.__obstacle_image = pygame.transform.scale(pygame.image.load(OBSTACLE_HEX_OBSTACLE_IMAGE_PATH),
                                                       (HEX_RADIUS_X[0] * HEX_TILE_IMAGES_SCALE[0],
                                                        HEX_RADIUS_Y[0] * HEX_TILE_IMAGES_SCALE[1])
                                                       )

    def __draw_feature(self, screen, feature, is_tank_there) -> None:
        """Renders the hexagon on the screen and draw a white border around the hexagon"""
        pygame.draw.polygon(screen, feature.color, feature.corners)

        # todo: make this better; make images smaller when tank is on that position
        image: Surface | None = None
        match feature.type:
            case Entities.CATAPULT:
                image = self.__catapult_image
            case Entities.LIGHT_REPAIR:
                image = self.__light_repair_image
            case Entities.HARD_REPAIR:
                image = self.__hard_repair_image
            # case Entities.EMPTY:
            #     image = self.__empty_image
            # case Entities.OBSTACLE:
            #     image = self.__obstacle_image
        if image is not None:
            x = feature.center[0] - image.get_width() / 2
            y = feature.center[1] - image.get_height() / 2
            screen.blit(image, (x, y))

        pygame.draw.aalines(screen, WHITE, closed=True, points=feature.corners)

    def __draw_legend(self, screen: Surface) -> None:
        y = 0
        for feature in self.__map_legend_items:
            if self.__font:
                text = self.__font.render(' ' + str(feature.type), True, WHITE)
                text_rect = text.get_rect(midleft=(feature.center[0] + HEX_RADIUS_X[0], feature.center[1]))
                screen.blit(text, text_rect)
            y += 2 * HEX_RADIUS_Y[0]
            self.__draw_feature(screen, feature, False)

    """Adding sprites to their group"""

    def add_explosion(self, tank: Tank, target: Tank) -> None:
        self.__max_damage_points = \
            max(self.__max_damage_points, self.__players[tank.player_index].damage_points)

        self.__explosion_group_buf.put(target.coord)

    def add_shot(self, start_pos: tuple[int, int], end_pos: tuple[int, int], color: tuple[int, int, int]) -> None:
        self.__projectile_group_buf.put((start_pos, end_pos, color))

    def add_hitreg(self, coords: tuple[int, int], image_path: str, color: str | tuple[int, int, int]):
        self.__shot_tanks_group_buf.put((coords, image_path, color))
