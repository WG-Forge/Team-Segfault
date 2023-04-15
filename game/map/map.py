import heapq

import pygame
from matplotlib import pyplot as plt
from pygame import Surface

from entity.map_features.base import Base
from entity.map_features.empty import Empty
from entity.map_features.obstacle import Obstacle
from entity.map_features.spawn import Spawn
from entity.tanks.tank import Tank
from entity.tanks.tank_maker import TankMaker
from map.hex import Hex


class Map:
    def __init__(self, client_map: dict, game_state: dict, active_players: dict):
        self.__players = Map.__add_players(active_players)
        self.__tanks: dict[int, Tank] = {}
        self.__map: dict = {}
        self.__base_coords: tuple = ()
        self.__make_map(client_map, game_state, active_players)
        _ = plt.figure()

    @staticmethod
    def __add_players(active_players: dict) -> tuple:
        players = [None, None, None]
        for player_id, player in active_players.items():
            if not player.is_observer:
                players[player.get_index()] = player
        return tuple(players)

    def __make_map(self, client_map: dict, game_state: dict, active_players: dict) -> None:
        # Make empty map
        rings = [Hex.make_ring(ring_num) for ring_num in range(client_map["size"])]
        self.__map = {coord: {'feature': Empty(coord), 'tank': None} for ring in rings for coord in ring}

        # put tanks in tanks & map & put spawns in map
        for vehicle_id, vehicle_info in game_state["vehicles"].items():
            player = active_players[vehicle_info["player_id"]]
            tank, spawn = TankMaker.create_tank(int(vehicle_id), vehicle_info, player.get_color(), player.get_index())
            tank_coord = tank.get_coord()
            self.__map[tank_coord]['tank'] = tank
            self.__map[tank_coord]['feature'] = spawn
            self.__tanks[int(vehicle_id)] = tank
            player.add_tank(tank)

        print(client_map["content"].items())

        # Put bases in map
        for entity, info in client_map["content"].items():
            print(entity)
            if entity == "base":
                self.__set_base(info)
            if entity == 'obstacle':
                self.__set_obstacles(info)
            else:
                print("Support for other entities needed")

    def __set_base(self, coords: dict) -> None:
        self.__base_coords = tuple([tuple(coord.values()) for coord in coords])
        for coord in self.__base_coords:
            self.__map[coord]['feature'] = Base(coord)

    def __set_obstacles(self, obstacles: []) -> None:
        for d in obstacles:
            coord = (d['x'], d['y'], d['z'])
            self.__map[coord]['feature'] = Obstacle(coord)

    def update_game_state(self, game_state: dict) -> None:
        # Updates the map information based on passed dictionary

        for vehicle_id, vehicle_info in game_state["vehicles"].items():
            vehicle_id = int(vehicle_id)
            action_coord = (vehicle_info["position"]["x"], vehicle_info["position"]["y"], vehicle_info["position"]["z"])

            tank = self.__tanks[vehicle_id]
            old_coord = tank.get_coord()
            tank.update(vehicle_info["health"], vehicle_info["capture_points"])
            if old_coord != action_coord:
                self.move(tank, action_coord)  # this tank did move -> update its position

    def move(self, tank: Tank, new_coord: tuple) -> None:
        old_coord = tank.get_coord()
        self.__map[new_coord]['tank'] = tank  # New pos has now tank
        self.__map[old_coord]['tank'] = None  # Old pos is now empty
        tank.set_coord(new_coord)  # tank has new position

    def shoot(self, tank: Tank, target: Tank):
        is_killed = target.reduce_hp()
        if is_killed:
            self.move(tank, tank.get_spawn_coord())

    def _is_others_spawn(self, spawn_coord: tuple, tank_id: int) -> bool:
        # If the feature at spawn_coord is a spawn object and it does not belong to the tank with tank_id return True
        feature = self.__map[spawn_coord]['feature']
        if isinstance(feature, Spawn):
            if feature.get_belongs_id() != tank_id:
                return True
        return False

    def get_players(self):
        return self.__players

    def get_player(self, index: int):
        return self.__players[index]

    def is_obstacle(self, coord: tuple) -> bool:
        return True if coord in self.__map and isinstance(self.__map[coord]['feature'], Obstacle) else False

    def __has_tank(self, coord: tuple) -> bool:
        return False if self.__map[coord]['tank'] is None else True

    def closest_base(self, to_where_coord: tuple) -> None:
        free_base_coords = tuple(coord for coord in self.__base_coords
                                 if self.__map[coord]['tank'] is None or coord == to_where_coord)
        if not free_base_coords:
            return None
        return min(free_base_coords, key=lambda coord: Hex.manhattan_dist(to_where_coord, coord))

    def closest_enemy(self, tank: Tank) -> Tank:
        friendly_index = tank.get_player_index()
        enemies = []
        for player in self.__players:
            if player is not None and player.get_index() != friendly_index:
                enemies.append(player)

        friend_coord = tank.get_coord()
        close_enemy_coord = (1000, 1000, 1000)
        close_enemy_dist = 1000
        for enemy in enemies:
            enemy_tanks = enemy.get_tanks()
            for enemy_tank in enemy_tanks:
                enemy_coord = enemy_tank.get_coord()
                distance = Hex.manhattan_dist(enemy_coord, friend_coord)
                if distance < close_enemy_dist:
                    close_enemy_coord = enemy_coord
                    close_enemy_dist = distance

        if close_enemy_dist != 1000:
            return self.__map[close_enemy_coord]['tank']
        else:
            print("no enemies, this is a single-player game")
            # raise KeyError("No enemy found, impossible, must be 10 enemies at all times")

    def next_best(self, tank: Tank, finish: tuple):
        start = tank.get_coord()
        tank_id = tank.get_id()
        speed = tank.get_speed()

        passable_obstacles = []
        cnt = 0

        while cnt < 25:
            frontier = []
            heapq.heappush(frontier, (0, start))
            came_from = {}
            cost_so_far = {start: 0}
            came_from[start] = None
            while frontier:
                current = heapq.heappop(frontier)[1]
                if current == finish:
                    break

                for movement in Hex.movements:
                    next_coord = Hex.coord_sum(current, movement)

                    if next_coord not in self.__map:  # If next does not exist in map, continue
                        continue
                    elif self.is_obstacle(next_coord) or next_coord in passable_obstacles:
                        # Then, check if it is an obstacle
                        continue

                    new_cost = cost_so_far[current] + 1
                    if next_coord not in cost_so_far or new_cost < cost_so_far[next_coord]:
                        cost_so_far[next_coord] = new_cost
                        priority = new_cost + Hex.manhattan_dist(finish, next_coord)
                        heapq.heappush(frontier, (priority, next_coord))
                        came_from[next_coord] = current

            path = []
            current = finish
            while current != start:
                path.append(current)
                if current not in came_from:
                    return None
                current = came_from[current]
            path.append(start)
            path.reverse()

            next_best = path[min(speed, len(path) - 1)]

            # If next_best is a tank or base, append to passable_obstacles and try again
            if self._is_others_spawn(next_best, tank_id) or self.__has_tank(next_best):
                passable_obstacles.append(next_best)
                cnt += 1
                continue
            else:
                return next_best

    def draw(self, screen: Surface):
        feature_hexes: [] = []

        plt.clf()
        for coord, entities in self.__map.items():
            feature, tank = entities['feature'], entities['tank']
            # Draw tank if any
            if tank is not None:
                color = tank.get_color()
                marker = tank.get_symbol()
                x, y = feature.get_center()

                # draw tank
                plt.plot(x, y, marker=marker, markersize='6', markerfacecolor=color, markeredgewidth=0.0)
                plt.text(x, y, str(tank.get_hp()), color='magenta', fontsize=10)

            feature.render(screen)
            feature_hexes.append(feature)
            # if isinstance(feature, Base) or isinstance(feature, Spawn) or isinstance(feature, Obstacle):
            #     feature_hexes.append(feature)
            #     continue
            # Draw the base hexes underneath
            # feature.render(screen)
            # feature.render_highlight(screen)
            xs, ys = zip(*feature.get_corners())
            plt.plot(xs, ys, feature.get_color())

        for feature in feature_hexes:
            # Draw the rest on top
            # feature.render(screen)
            feature.render_highlight(screen)
            xs, ys = zip(*feature.get_corners())
            plt.plot(xs, ys, feature.get_color())

        plt.axis('off')
        # comment this if using SciView
        plt.pause(2)
        plt.draw()
