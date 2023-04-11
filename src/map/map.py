from matplotlib import pyplot as plt

from entity.map_features.base import Base
from entity.map_features.empty import Empty
from entity.map_features.obstacle import Obstacle
from entity.map_features.spawn import Spawn
from entity.tanks.tank import Tank
from src.map.hex import Hex


class Map:
    def __init__(self, size: int):
        # __map = {(0,0,0) : obj[] -> {'feature': Base or Obstacle..., 'tank': Tank or None], (-1,0,-1): {...}}
        self.__map: dict = self.__make_map(size)
        self.__base_coords: tuple = ()
        self.__players = ()

    def __make_map(self, size):
        rings = [Hex.make_ring_coords(ring_num) for ring_num in range(size)]
        return {coord: {'feature': Empty(coord), 'tank': None} for ring in rings for coord in ring}

    def get_feature_at(self, coord: tuple):
        return self.__map[coord]['feature']

    def get_tank(self, coord: tuple):
        return self.__map[coord]['tank']

    def set_tank(self, tank: Tank, coord: tuple) -> None:
        self.__map[tank.get_coord()]['tank'] = None  # Old pos is now empty
        self.__map[coord]['tank'] = tank  # New pos has now tank
        tank.set_coord(coord)  # tank has new position

    def set_base(self, coords: dict) -> None:
        #TODO: take away the adjacent edge of empty hexes next to base
        self.__base_coords = tuple([tuple(coord.values()) for coord in coords])
        for coord in self.__base_coords:
            self.__map[coord]['feature'] = Base(coord)

    def set_spawn(self, spawn: Spawn, coord: tuple) -> None:
        self.__map[coord]['feature'] = spawn

    def set_obstacle(self, coord: tuple) -> None:
        self.__map[coord]['feature'] = Obstacle(coord)

    def is_others_spawn(self, coord: tuple, tank_id: int) -> bool:
        feature = self.__map[coord]['feature']
        if isinstance(feature, Spawn):
            if feature.get_belongs_id() != tank_id:
                return True
        return False

    def is_obstacle(self, coord: tuple) -> bool:
        return True if isinstance(self.__map[coord]['feature'], Obstacle) else False

    def is_occupied(self, coord: tuple) -> bool:
        return False if self.__map[coord]['tank'] is None else True

    def has(self, coord: tuple) -> bool:
        return coord in self.__map

    def closest_base(self, to_where_coord: tuple) -> tuple:
        free_base_coords = tuple(coord for coord in self.__base_coords if self.__map[coord]['tank'] is None)
        if not free_base_coords:
            return None
        return min(free_base_coords, key=lambda coord: Hex.abs_dist(to_where_coord, coord))

    def closest_enemy(self, friendly_tank: Tank) -> Tank:
        friendly_index = friendly_tank.get_player_index()
        enemies = []
        for player in self.__players:
            if player.get_index() != friendly_index:
                enemies.append(player)

        friendly_tank_coord = friendly_tank.get_coord()
        closest_tank_coord = (1000, 1000, 1000)
        closest_tank_dist = 1000
        for enemy in enemies:
            enemy_tanks = enemy.get_tanks()
            for enemy_tank in enemy_tanks:
                enemy_tank_coord = enemy_tank.get_coord()
                distance = Hex.abs_dist(enemy_tank.get_coord(), friendly_tank_coord)
                if distance < closest_tank_dist:
                    closest_tank_coord = enemy_tank_coord
                    closest_tank_dist = distance

        if closest_tank_dist != 1000:
            return self.__map[closest_tank_coord]['tank']

    def set_players(self, players: tuple) -> None:
        self.__players = players

    def draw(self):
        feature_hexes: [] = []
        plt.figure()
        for coord, entities in self.__map.items():
            feature, tank = entities['feature'], entities['tank']
            # Draw tank if any
            if tank is not None:
                color = tank.get_colour()
                marker = tank.get_symbol()
                x, y = feature.get_center()
                plt.plot(x, y, marker=marker, markersize='6', markerfacecolor=color, markeredgewidth=0.0)

            if isinstance(feature, Base) or isinstance(feature, Spawn) or isinstance(feature, Obstacle):
                feature_hexes.append(feature)
                continue
            # Draw feature
            xs, ys = zip(*feature.get_corners())
            plt.plot(xs, ys, feature.get_color())

        for feature in feature_hexes:
            xs, ys = zip(*feature.get_corners())
            plt.plot(xs, ys, feature.get_color(), fillstyle='none')

        plt.axis('off')
        # comment this if using SciView
        plt.pause(2)
        plt.show(block=False)
        plt.close("all")
