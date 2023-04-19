import heapq

import pygame
from pygame import Surface

from consts import SCREEN_HEIGHT, SCREEN_WIDTH
from entity.map_features.base import Base
from entity.map_features.empty import Empty
from entity.map_features.obstacle import Obstacle
from entity.map_features.spawn import Spawn
from entity.tanks.tank import Tank
from entity.tanks.tank_maker import TankMaker
from map.hex import Hex
from pygame_utils.explosion import Explosion
from pygame_utils.scoreboard import Scoreboard


class Map:
    def __init__(self, client_map: dict, game_state: dict, active_players: dict):
        self.__players = Map.__add_players(active_players)
        self.__tanks: dict[int, Tank] = {}
        self.__map: dict = {}
        self.__base_coords: tuple = ()
        self.__make_map(client_map, game_state, active_players)
        self.__num_of_radii: int = (client_map["size"] - 1) * 2 * 2
        self.__turn: list[1] = [-1]
        self.__max_damage_points: int = 0

        self.__scoreboard = Scoreboard(self.__players)
        Hex.radius_x = SCREEN_WIDTH // self.__num_of_radii  # number of half radii on x axis
        Hex.radius_y = SCREEN_HEIGHT // self.__num_of_radii
        self.__scoreboard.update_image_size(Hex.radius_x * 2, Hex.radius_y * 2)
        self.__scoreboard.set_radii(Hex.radius_x / 3, Hex.radius_y / 3)

        self.__font_size = round(1.2 * min(Hex.radius_y, Hex.radius_x))

        self.__explosion_group = pygame.sprite.Group()

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
            cost_so_far = {}
            came_from[start] = None
            cost_so_far[start] = 0
            while frontier:
                current = heapq.heappop(frontier)[1]
                if current == finish:
                    break

                for movement in Hex.movements:
                    next = Hex.coord_sum(current, movement)

                    if next not in self.__map:  # If next does not exist in map, continue
                        continue
                    elif self.is_obstacle(next) or next in passable_obstacles:  # Then, check if it is an obstacle
                        continue

                    new_cost = cost_so_far[current] + 1
                    if next not in cost_so_far or new_cost < cost_so_far[next]:
                        cost_so_far[next] = new_cost
                        priority = new_cost + Hex.manhattan_dist(finish, next)
                        heapq.heappush(frontier, (priority, next))
                        came_from[next] = current

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
            if self.__is_others_spawn(next_best, tank_id) or self.__has_tank(next_best):
                passable_obstacles.append(next_best)
                cnt += 1
                continue
            else:
                return next_best

    def sync_local_with_server(self, game_state: dict) -> None:
        # Updates the map information based on passed dictionary from server map

        for vehicle_id, vehicle_info in game_state["vehicles"].items():
            vehicle_id = int(vehicle_id)
            server_coord = (vehicle_info["position"]["x"], vehicle_info["position"]["y"], vehicle_info["position"]["z"])
            server_hp = vehicle_info['health']
            server_cp = vehicle_info["capture_points"]

            tank = self.__tanks[vehicle_id]
            local_coord = tank.get_coord()
            local_hp = tank.get_hp()
            local_cp = tank.get_cp()

            if server_coord != local_coord:
                self.move(tank, server_coord)
            if server_hp != local_hp:
                tank.update_hp(server_hp)
            if server_cp != local_cp:
                tank.update_cp(server_cp)

    def move(self, tank: Tank, new_coord: tuple) -> None:
        old_coord = tank.get_coord()
        self.__map[new_coord]['tank'] = tank  # New pos has now tank
        self.__map[old_coord]['tank'] = None  # Old pos is now empty
        tank.set_coord(new_coord)  # tank has new position

    def shoot(self, tank: Tank, target: Tank):
        destroyed = target.register_hit_return_destroyed()
        if destroyed:
            # add explosion
            explosion = Explosion(target.get_screen_position(), Hex.radius_x * 2, Hex.radius_y * 2)
            self.__explosion_group.add(explosion)

            self.move(target, target.get_spawn_coord())
            self.__players[tank.get_player_index()].register_destroyed_vehicle(target)
            self.__max_damage_points = \
                max(self.__max_damage_points, self.__players[tank.get_player_index()].get_damage_points())

        self.__players[tank.get_player_index()].register_shot(target.get_player_index())

    def can_shoot(self, player_index: int, enemy_index: int) -> bool:
        other_index = next(iter({0, 1, 2} - {player_index, enemy_index}))
        enemy = self.__players[enemy_index]
        other = self.__players[other_index]

        enemy_shot_player = enemy.has_shot(player_index)
        other_shot_enemy = other.has_shot(enemy_index)
        can_shoot = enemy_shot_player or not other_shot_enemy

        # print(
        #     f'(E:{enemy_index}->P:{player_index}) = {enemy_shot_player} or not (O:{other_index}->E:{enemy_index}) = {other_shot_enemy} can_shoot = {can_shoot}')

        return can_shoot

    def get_players(self):
        return self.__players

    def get_player(self, index: int):
        return self.__players[index]

    def is_obstacle(self, coord: tuple) -> bool:
        return True if coord in self.__map and isinstance(self.__map[coord]['feature'], Obstacle) else False

    def closest_base(self, to_where_coord: tuple) -> tuple or None:
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

    def __make_map(self, client_map: dict, game_state: dict, active_players: dict):
        # Make empty map
        rings = [Hex.make_ring(ring_num) for ring_num in range(client_map["size"])]
        self.__map = {coord: {'feature': Empty(coord), 'tank': None} for ring in rings for coord in ring}

        # put tanks in tanks & map & put spawns in map
        for vehicle_id, vehicle_info in game_state["vehicles"].items():
            player = active_players[vehicle_info["player_id"]]
            tank, spawn = TankMaker.create_tank_and_spawn(int(vehicle_id), vehicle_info, player.get_color(),
                                                          player.get_index())
            tank_coord = tank.get_coord()
            self.__map[tank_coord]['tank'] = tank
            self.__map[tank_coord]['feature'] = spawn
            self.__tanks[int(vehicle_id)] = tank
            player.add_tank(tank)

        # Put entities in map
        for entity, info in client_map["content"].items():
            if entity == "base":
                self.__set_base(info)
            elif entity == 'obstacle':
                self.__set_obstacles(info)
            else:
                print(f"Support for {entity} needed")

    def __is_others_spawn(self, spawn_coord: tuple, tank_id: int) -> bool:
        # If the feature at spawn_coord is a spawn object and it does not belong to the tank with tank_id return True
        feature = self.__map[spawn_coord]['feature']
        if isinstance(feature, Spawn):
            if feature.get_belongs_id() != tank_id:
                return True
        return False

    def __has_tank(self, coord: tuple) -> bool:
        return False if self.__map[coord]['tank'] is None else True

    def __set_base(self, coords: dict) -> None:
        self.__base_coords = tuple([tuple(coord.values()) for coord in coords])
        for coord in self.__base_coords:
            self.__map[coord]['feature'] = Base(coord)

    def __set_obstacles(self, obstacles: []) -> None:
        for d in obstacles:
            coord = (d['x'], d['y'], d['z'])
            self.__map[coord]['feature'] = Obstacle(coord)

    @staticmethod
    def __add_players(active_players: dict) -> tuple:
        players = [None, None, None]
        for player_id, player in active_players.items():
            if not player.is_observer:
                players[player.get_index()] = player
        return tuple(players)

    def set_turn_reference(self, turn: list[1]) -> None:
        self.__turn = turn
