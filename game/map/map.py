import heapq
from typing import List, Union

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
        self.__tanks: dict[str, Tank] = {}
        self.__map: dict = {}
        self.__base_coords: tuple = ()
        self.__spawn_coords: tuple = ()
        self.__make_map(client_map, game_state, active_players)
        self.__destroyed: List[Tank] = []
        _ = plt.figure()

    """     MAP MAKING      """

    def __make_map(self, client_map: dict, game_state: dict, active_players: dict) -> None:
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
            self.__tanks[vehicle_id] = tank
            player.add_tank(tank)

        # Put entities in map
        for entity, info in client_map["content"].items():
            if entity == "base":
                self.__make_bases(info)
            elif entity == 'obstacle':
                self.__make_obstacles(info)
            else:
                print(f"Support for {entity} needed")

    @staticmethod
    def __add_players(active_players: dict) -> tuple:
        players = [None, None, None]
        for player_id, player in active_players.items():
            if not player.is_observer:
                players[player.get_index()] = player
        return tuple(players)

    def __make_bases(self, coords: dict) -> None:
        self.__base_coords = tuple([tuple(coord.values()) for coord in coords])
        for coord in self.__base_coords:
            self.__map[coord]['feature'] = Base(coord)

    def __make_obstacles(self, obstacles: []) -> None:
        for d in obstacles:
            coord = (d['x'], d['y'], d['z'])
            self.__map[coord]['feature'] = Obstacle(coord)

    """     SYNCHRONISE SERVER AND LOCAL MAPS        """

    def sync_local_with_server(self, game_state: dict) -> None:
        for vehicle_id, vehicle_info in game_state["vehicles"].items():
            server_coord = (vehicle_info["position"]["x"], vehicle_info["position"]["y"], vehicle_info["position"]["z"])
            server_hp, server_cp = vehicle_info['health'], vehicle_info["capture_points"]

            tank = self.__tanks[vehicle_id]
            self.local_move(tank, server_coord) if server_coord != tank.get_coord() else None
            tank.set_hp(server_hp) if server_hp != tank.get_hp() else None
            tank.set_cp(server_cp) if server_cp != tank.get_cp() else None

    """     MOVE & FIRE CONTROL        """

    def local_move(self, tank: Tank, new_coord: tuple) -> None:
        old_coord = tank.get_coord()
        self.__map[new_coord]['tank'] = tank  # New pos has now tank
        self.__map[old_coord]['tank'] = None  # Old pos is now empty
        tank.set_coord(new_coord)  # tank has new position

    def local_shoot(self, tank: Tank, target: Tank) -> None:
        destroyed = target.register_hit_return_destroyed()
        if destroyed:
            self.__destroyed.append(target)
        self.__players[tank.get_player_index()].register_shot(target.get_player_index())

    def td_shoot(self, td: Tank, target: tuple) -> None:
        danger_zone = Hex.danger_zone(td.get_coord(), target)
        for coord in danger_zone:
            entities = self.__map.get(coord)
            if entities and not isinstance(entities['feature'], Obstacle):
                enemy = self.__map[coord]['tank']
                if enemy and not (td.get_player_index() == enemy.get_player_index() or
                                  self.is_neutral(td, enemy) or enemy.is_destroyed()):
                    self.local_shoot(td, enemy)
            else:
                break

    def respawn_destroyed_tanks(self) -> None:
        while self.__destroyed:
            tank = self.__destroyed.pop()
            self.local_move(tank, tank.get_spawn_coord())
            tank.respawn()

    def is_neutral(self, player_tank: Tank, enemy_tank: Tank) -> bool:
        # Neutrality rule logic implemented here, return True if not neutral, False if neutral
        player_index, enemy_index = player_tank.get_player_index(), enemy_tank.get_player_index()
        other_index = next(iter({0, 1, 2} - {player_index, enemy_index}))
        other_player, enemy_player = self.__players[other_index], self.__players[enemy_index]
        return not enemy_player.has_shot(player_index) and other_player.has_shot(enemy_index)

    """     NAVIGATION    """

    def closest_base(self, to: tuple) -> Union[tuple, None]:
        free_base_coords = tuple(c for c in self.__base_coords if self.__map[c]['tank'] is None or c == to)
        if free_base_coords:
            return min(free_base_coords, key=lambda coord: Hex.manhattan_dist(to, coord))

    def closest_enemies(self, tank: Tank) -> List[Tank]:
        # Returns a sorted list by distance of enemy tanks
        tank_idx, tank_coord = tank.get_player_index(), tank.get_coord()
        enemies = [player for player in self.__players if player.get_index() != tank_idx]
        return sorted((enemy_tank for enemy in enemies for enemy_tank in enemy.get_tanks()),
                      key=lambda enemy_tank: Hex.manhattan_dist(enemy_tank.get_coord(), tank_coord))

    def next_best_available_hex_in_path_to(self, tank: Tank, finish: tuple) -> Union[tuple, None]:
        start, tank_id, speed = tank.get_coord(), tank.get_id(), tank.get_speed()
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
                    coord = Hex.coord_sum(current, movement)
                    entities = self.__map.get(coord)
                    if entities and not (isinstance(entities['feature'], Obstacle) or coord in passable_obstacles):
                        new_cost = cost_so_far[current] + 1
                        if coord not in cost_so_far or new_cost < cost_so_far[coord]:
                            cost_so_far[coord] = new_cost
                            priority = new_cost + Hex.manhattan_dist(finish, coord)
                            heapq.heappush(frontier, (priority, coord))
                            came_from[coord] = current
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
            if self._is_others_spawn(next_best, tank_id) or self.__map[next_best]['tank']:
                passable_obstacles.append(next_best)
                cnt += 1
                continue
            else:
                return next_best

    def _is_others_spawn(self, spawn_coord: tuple, tank_id: int) -> bool:
        # If the feature at spawn_coord is a spawn object and it does not belong to the tank with tank_id return True
        feature = self.__map[spawn_coord]['feature']
        if isinstance(feature, Spawn):
            if feature.get_belongs_id() != tank_id:
                return True
        return False

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
        plt.pause(0.25)
        plt.draw()
