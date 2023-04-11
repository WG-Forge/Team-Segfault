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
        self.__size = size

    def __make_map(self, size):
        rings = [Hex.make_ring_coords(ring_num) for ring_num in range(size)]
        return {coord: {'feature': Empty(coord), 'tank': None} for ring in rings for coord in ring}

    def get_feature_at(self, coord: tuple):
        return self.__map[coord]['feature']

    def get_tank_at(self, coord: tuple):
        return self.__map[coord]['tank']

    def set_tank_at(self, tank: Tank, coord: tuple) -> None:
        self.__map[tank.get_coord()]['tank'] = None  # Old pos is now empty
        self.__map[coord]['tank'] = tank  # New pos has now tank
        tank.set_coord(coord)  # tank has new position

    def set_base(self, coords: dict) -> None:
        self.__base_coords = tuple([tuple(coord.values()) for coord in coords])
        for coord in self.__base_coords:
            self.__map[coord]['feature'] = Base(coord)

    def set_spawn(self, coord: tuple) -> None:
        self.__map[coord]['feature'] = Spawn(coord)

    def set_obstacle(self, coord: tuple) -> None:
        self.__map[coord]['feature'] = Obstacle(coord)

    def get_base_coords(self) -> tuple:
        return self.__base_coords

    def is_base(self, coord: tuple) -> bool:
        return True if isinstance(self.__map[coord]['feature'], Base) else False

    def get_closest_base_coord(self, tank: Tank) -> tuple:
        free_base_coords = tuple(coord for coord in self.__base_coords if self.__map[coord]['tank'] is None)
        if not free_base_coords:
            return None
        tank_coord = tank.get_coord()
        return min(free_base_coords, key=lambda coord: Hex.abs_dist(tank_coord, coord))

    def is_valid(self, coord: tuple) -> bool:
        ring_num = sum(abs(c) for c in coord) / 2
        # May be inefficient due to last condition always being true but untested
        if sum(coord) == 0 and ring_num <= self.__size and all(abs(c) <= ring_num for c in coord):
            # print('True')
            return True
        # print('False')
        return False

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
