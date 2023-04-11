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
        cnt = 0

        # TODO: make more efficient
        while cnt < 15:
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
                cnt += 1
                continue
            else:
                return next_best


    def set_tanks(self, tanks: dict[int: Tank]):
        self.__tanks = tanks  # Tanks set from Game

    def get_map(self) -> tuple:
        return self.__map
