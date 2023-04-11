import heapq
from collections import defaultdict
from sortedcontainers import SortedSet

from entity.tanks.tank_maker import TankMaker
from map.hex import Hex
from map.map import Map
from src.client.server_enum import Action
from src.entity.tanks.tank import Tank


class GameMap:
    __movements = ((1, 0, -1), (0, 1, -1), (1, -1, 0), (-1, 0, 1), (0, -1, 1), (-1, 1, 0))

    def __init__(self, client_map: dict, game_state: dict, active_players: dict):
        self.__tanks: dict[int, Tank] = {}
        self.__map = self.parse_map(client_map, game_state, active_players)

    def parse_map(self, client_map: dict, game_state: dict, active_players: dict) -> Map:
        parsed_map = Map(client_map["size"])

        # put tanks in self.__tanks & add tanks to players
        for vehicle_id, vehicle_info in game_state["vehicles"].items():
            player = active_players[vehicle_info["player_id"]]
            player_colour = player.get_colour()
            tank, spawn = TankMaker.create_tank(int(vehicle_id), vehicle_info, player_colour)
            self.__tanks[int(vehicle_id)] = tank
            tank_coord = tank.get_coord()
            parsed_map.set_tank(tank, tank_coord)
            parsed_map.set_spawn(spawn, tank_coord)
            player.add_tank(tank)

        for entity, coords in client_map["content"].items():
            if entity == "base":
                parsed_map.set_base(coords)
            else:
                print("Support for other entities needed")

        return parsed_map

    def update(self, game_state: dict) -> None:
        """
         Updates the map information based on passed dictionary
        :param game_state: either a GAME_STATE dict or GAME_ACTIONS dict
        :return: None
        """
        if "actions" in game_state:
            # todo make another function that updates tank positions only
            for action in game_state["actions"]:
                data = action["data"]
                tank_id = data["vehicle_id"]
                action_coord: tuple = (data['target']['x'], data['target']['y'], data['target']['z'])

                tank = self.__tanks[tank_id]
                if action["action_type"] == Action.MOVE:
                    self.__map.set_tank(tank, action_coord)

                if action["action_type"] == Action.SHOOT:
                    shot_tank = self.__map.get_tank(action_coord)
                    if shot_tank.reduce_hp():
                        self.__map.set_tank(shot_tank, shot_tank.get_spawn_coord)
            return

        vehicles = game_state["vehicles"]
        for vehicle_id, vehicle_info in vehicles.items():
            vehicle_id = int(vehicle_id)
            action_coord = (vehicle_info["position"]["x"], vehicle_info["position"]["y"], vehicle_info["position"]["z"])

            if vehicle_id in self.__tanks:
                tank = self.__tanks[vehicle_id]
                old_coord = tank.get_coord()
                tank.update(vehicle_info["health"], vehicle_info["capture_points"])
                if old_coord != action_coord:
                    self.__map.set_tank(tank, action_coord)  # this tank did move -> update its position

    def draw_map(self) -> None:
        self.__map.draw()

    def next_best(self, start: tuple, finish: tuple, speed: int, tank_id: int):
        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0
        passable_obstacles = []

        # TODO: Add support for impossible paths eg. blocked tank
        while True:
            while frontier:
                current = heapq.heappop(frontier)[1]

                if current == finish:
                    break

                for movement in GameMap.__movements:
                    next = Hex.coord_sum(current, movement)

                    if not self.__map.has(next): # First check if next exists in map
                        continue
                    elif self.__map.is_obstacle(next) or next in passable_obstacles: # Then, check if it is an obstacle
                        continue

                    new_cost = cost_so_far[current] + 1
                    if next not in cost_so_far or new_cost < cost_so_far[next]:
                        cost_so_far[next] = new_cost
                        priority = new_cost + Hex.abs_dist(finish, next)
                        heapq.heappush(frontier, (priority, next))
                        came_from[next] = current

            path = []
            current = finish
            while current != start:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()

            if speed >= len(path):
                speed = len(path)-1
            next_best = path[speed]

            # If next_best is a tank or base, append to passable_obstacles and try again
            if self.__map.is_others_spawn(next_best, tank_id) or self.__map.is_occupied(next_best):
                passable_obstacles.append(next_best)
                continue
            else:
                return next_best

    def shortest_path(self, start: tuple, end: tuple) -> [tuple]:
        """
        Determines the shortest path between two coords(x,y,z)
        :param start: start hex
        :param end: target hex
        :return: list of hexes that represent the shortest path
        """
        # O(log n) adding, removing and finding the best hex
        open_list = SortedSet()
        open_list.add((Hex.abs_dist(end, start), start))

        # O(1) checking if hex is in the open_list
        open_list_check: dict[tuple, bool] = {start: True}
        closed_list: dict[tuple, bool] = {}
        parent: dict = {start: None}

        movements = ((1, 0, -1), (0, 1, -1), (1, -1, 0), (-1, 0, 1), (0, -1, 1), (-1, 1, 0))

        cheapest_path = defaultdict(lambda: float('inf'))
        cheapest_path[start] = 0

        path_found = False
        while len(open_list) > 0:
            # get the next best coord
            current = open_list[0][1]
            if current == end:
                path_found = True
                break
            for movement in movements:
                neighbour = Hex.coord_sum(current, movement)

                if not self.__map.is_valid(neighbour):
                    continue

                path_to_neighbour_cost = cheapest_path[current] + 1
                if (neighbour not in open_list_check or open_list_check[neighbour] is False) \
                        and (neighbour not in closed_list or closed_list[neighbour] is False):
                    open_list.add((Hex.abs_dist(end, neighbour) + path_to_neighbour_cost, neighbour))
                    open_list_check[neighbour] = True
                    parent[neighbour] = current
                    cheapest_path[neighbour] = path_to_neighbour_cost
                elif path_to_neighbour_cost < cheapest_path[neighbour]:
                    parent[neighbour] = current
                    cheapest_path[neighbour] = path_to_neighbour_cost
                    if neighbour in closed_list and closed_list[neighbour] is True:
                        closed_list[neighbour] = False
                        open_list.add((Hex.abs_dist(end, neighbour) + path_to_neighbour_cost, neighbour))
                        open_list_check[neighbour] = True

            open_list.pop(0)
            open_list_check[current] = False
            closed_list[current] = True

        if path_found:
            path: [] = []
            while end is not None:
                path.append(end)
                end = parent[end]
            path.reverse()
            return tuple(path)
        else:
            return ()

    def set_tanks(self, tanks: dict[int: Tank]):
        self.__tanks = tanks  # Tanks set from Game

    def get_map(self) -> tuple:
        return self.__map
