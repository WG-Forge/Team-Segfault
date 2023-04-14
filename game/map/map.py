import heapq

from matplotlib import pyplot as plt

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

    def __make_map(self, client_map: dict, game_state: dict, active_players: dict) -> dict:
        # Make empty map
        rings = [Hex.make_ring(ring_num) for ring_num in range(client_map["size"])]
        self.__map = {coord: {'feature': Empty(coord), 'tank': None} for ring in rings for coord in ring}

        # put tanks in tanks & map & put spawns in map
        for vehicle_id, vehicle_info in game_state["vehicles"].items():
            player = active_players[vehicle_info["player_id"]]
            tank, spawn = TankMaker.create_tank_and_spawn(int(vehicle_id), vehicle_info, player.get_color(), player.get_index())
            tank_coord = tank.get_coord()
            self.__map[tank_coord]['tank'] = tank
            self.__map[tank_coord]['feature'] = spawn
            self.__tanks[int(vehicle_id)] = tank
            player.add_tank(tank)

        # Put bases in map
        for entity, info in client_map["content"].items():
            if entity == "base":
                self.__set_base(info)
            elif entity == 'obstacle':
                self.__set_obstacles(info)
            else:
                print(f"Support for {entity} needed")

    def __set_base(self, coords: dict) -> None:
        self.__base_coords = tuple([tuple(coord.values()) for coord in coords])
        for coord in self.__base_coords:
            self.__map[coord]['feature'] = Base(coord)

    def __set_obstacles(self, obstacles: []) -> None:
        for d in obstacles:
            coord = (d['x'], d['y'], d['z'])
            self.__map[coord]['feature'] = Obstacle(coord)

    def update_game_state(self, game_state: dict) -> None:
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
                print('move update id', vehicle_id, 'local', local_coord, 'server', server_coord)
                self.move(tank, server_coord)
            if server_hp != local_hp:
                print('hp update')
                tank.update_hp(server_hp)
            if server_cp != local_cp:
                print('cp update')
                tank.update_cp(server_cp)

    def move(self, tank: Tank, new_coord: tuple) -> None:
        old_coord = tank.get_coord()
        self.__map[new_coord]['tank'] = tank  # New pos has now tank
        self.__map[old_coord]['tank'] = None  # Old pos is now empty
        tank.set_coord(new_coord)  # tank has new position

    def shoot(self, tank: Tank, target: Tank):
        destroyed = target.register_hit_return_destroyed()
        if destroyed:
            self.move(target, target.get_spawn_coord())
        self.__players[tank.get_player_index()].has_shot(target.get_player_index())

    def can_shoot(self, player_index: int, enemy_index: int) -> bool:
        other_index = next(iter({0, 1, 2} - {player_index, enemy_index}))
        enemy = self.__players[enemy_index]
        other = self.__players[other_index]

        enemy_shot_player = enemy.has_shot(player_index)
        other_shot_enemy = other.has_shot(enemy_index)

        return enemy_shot_player or not other_shot_enemy

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

    def closest_base(self, to_where_coord: tuple) -> tuple:
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
            if self._is_others_spawn(next_best, tank_id) or self.__has_tank(next_best):
                passable_obstacles.append(next_best)
                cnt += 1
                continue
            else:
                return next_best

    def draw(self):
        feature_hexes: [] = []

        plt.clf()
        for coord, entities in self.__map.items():
            feature, tank = entities['feature'], entities['tank']
            # Draw tank if any
            if tank is not None:
                color = tank.get_color()
                marker = tank.get_symbol()
                x, y = feature.get_center()
                plt.plot(x, y, marker=marker, markersize='6', markerfacecolor=color, markeredgewidth=0.0)
                plt.text(x, y, str(tank.get_hp()), color='magenta', fontsize=10)

            if isinstance(feature, Base) or isinstance(feature, Spawn) or isinstance(feature, Obstacle):
                feature_hexes.append(feature)
                continue
            # Draw feature
            xs, ys = zip(*feature.get_corners())
            plt.plot(xs, ys, feature.get_color())

        for feature in feature_hexes:
            xs, ys = zip(*feature.get_corners())
            plt.plot(xs, ys, feature.get_color())

        plt.axis('off')
        # comment this if using SciView
        plt.pause(0.5)
        plt.draw()

    @staticmethod
    def __add_players(active_players: dict) -> tuple:
        players = [None, None, None]
        for player_id, player in active_players.items():
            if not player.is_observer:
                players[player.get_index()] = player
        return tuple(players)

