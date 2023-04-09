from collections import defaultdict

import matplotlib.pyplot as plt
from sortedcontainers import SortedSet

from entity.base import Base
from src.client.server_enum import Action
from src.entity.entity import Entity
from src.entity.tanks.tank import Tank
from src.map.hex import Hex


class GameMap:
    def __init__(self, client_map: dict):
        self.__map_size: int = 0
        self.__entities: dict[Hex, Entity] = {}
        # tank_id -> hex
        self.__tank_positions: dict[int, Hex] = {}
        self.__tanks: dict[int, Tank] = {}
        # tanks_in_base could probably be deleted
        self.__tanks_in_base: list[int] = []
        #        self.__base: [Hex] = []
        self.parse_map(client_map)
        self.__base: Base

    def parse_map(self, client_map: dict) -> None:
        """
        Saves entity data
        :param client_map: dict of GAME_MAP response
        :return: None
        """
        self.__map_size = client_map["size"]
        for entity, coords in client_map["content"].items():
            if entity == "base":
                self.__base = Base(coords)
            else:
                print("Support for other entities needed")

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
                action_pos = Hex([data['target']['x'], data['target']['y'], data['target']['z']])

                tank = self.__tanks[tank_id]
                if action["action_type"] == Action.MOVE:
                    # if tank was in base before movement, remove it from tanks_in_base
                    if self.__base.is_in(tank.get_coords()):
                        self.__base.leave(tank.get_coords())

                    tank.set_pos(action_pos)

                    if self.__base.is_in(action_pos.get_coords()):
                        self.__base.occupy(action_pos.get_coords())
                    if self.__base.is_in(action_pos.get_coords()):
                        self.__tanks_in_base.append(tank_id)

                if action["action_type"] == Action.SHOOT:
                    shot_tank = self.tank_in_pos(action_pos)
                    if shot_tank.reduce_hp():
                        respawn_pos = shot_tank.get_spawn_pos()
                        shot_tank.set_pos(respawn_pos)
            return

        vehicles = game_state["vehicles"]
        for vehicle_id, vehicle_info in vehicles.items():
            vehicle_id = int(vehicle_id)
            action_pos = Hex([vehicle_info["position"]["x"],
                              vehicle_info["position"]["y"],
                              vehicle_info["position"]["z"]])

            if vehicle_id in self.__tanks:
                tank = self.__tanks[vehicle_id]
                old_position = tank.get_pos()
                if old_position == action_pos:
                    # this tank did not move, only update hp and capture points
                    tank.update(vehicle_info["health"], vehicle_info["capture_points"])
                else:
                    # this tank did move -> update its position and after that update its hp and capture points
                    if self.__base.is_in(old_position.get_coords()):
                        self.__base.leave(old_position.get_coords())

                    # tank moved to the base, append it to tanks_in_base list
                    if self.__base.is_in(action_pos.get_coords()):
                        self.__base.occupy(action_pos.get_coords())

                    # if light or hard repair was there, overwrite hex with this tank and
                    # update tank vehicle_info from server response
                    tank.update(vehicle_info["health"], vehicle_info["capture_points"])
                    tank.set_pos(action_pos)

    def draw_map(self) -> None:
        # TODO: optimize, adjacent hexes have some same edges & implement drawing obstacles
        plt.figure()
        # draw base
        base_coords = self.__base.get_coords()
        for coord in base_coords:
            xs, ys = zip(*Hex.get_corners(coord))
            plt.plot(xs, ys, 'g')

        # draw the whole map
        for x in range(-self.__map_size + 1, self.__map_size):
            for y in range(-self.__map_size + 1, self.__map_size):
                z = -x - y
                if self.__map_size > z > -self.__map_size and (x, y, z) not in base_coords:
                    xs, ys = zip(*Hex.get_corners((x, y, z)))
                    plt.plot(xs, ys, 'k')

        # Draw tanks
        for tank_id, tank in self.__tanks.items():
            colour = tank.get_colour()
            marker = tank.get_symbol()
            x, y = Hex.get_center(tank.get_coords())
            plt.plot(x, y, marker=marker, markersize='6', markerfacecolor=colour, markeredgewidth=0.0)

        plt.axis('off')
        # comment this if using SciView
        plt.pause(2)
        plt.show(block=False)
        plt.close("all")

    def shortest_path(self, start: Hex, end: Hex) -> [Hex]:
        """
        Determines the shortest path between two hexes
        :param start: start hex
        :param end: target hex
        :return: list of hexes that represent the shortest path
        """
        # O(log n) adding, removing and finding the best hex
        open_list = SortedSet()
        open_list.add((end - start, start))
        # O(1) checking if hex is in the open_list
        open_list_check: dict[Hex, bool] = {start: True}

        closed_list: dict[Hex, bool] = {}

        parent: dict = {start: None}

        movements = [
            Hex([1, 0, -1]),
            Hex([0, 1, -1]),
            Hex([1, -1, 0]),
            Hex([-1, 0, 1]),
            Hex([0, -1, 1]),
            Hex([-1, 1, 0])
        ]

        cheapest_path = defaultdict(lambda: float('inf'))
        cheapest_path[start] = 0

        path_found = False
        while len(open_list) > 0:
            # get the next best hex
            current = open_list[0][1]
            if current == end:
                path_found = True
                break
            for movement in movements:
                neighbour = current + movement
                if not self.is_valid(neighbour):# or \ #Uncomment when implementing obstacles
                        #(neighbour in self.__entities and self.__entities[neighbour].get_type() == 'obstacle'):
                    # if hex is out of bounds or if there is an obstacle on that hex, skip
                    continue
                path_to_neighbour_cost = cheapest_path[current] + 1
                if (neighbour not in open_list_check or open_list_check[neighbour] is False) \
                        and (neighbour not in closed_list or closed_list[neighbour] is False):
                    open_list.add((end - neighbour + path_to_neighbour_cost, neighbour))
                    open_list_check[neighbour] = True
                    parent[neighbour] = current
                    cheapest_path[neighbour] = path_to_neighbour_cost
                elif path_to_neighbour_cost < cheapest_path[neighbour]:
                    parent[neighbour] = current
                    cheapest_path[neighbour] = path_to_neighbour_cost
                    if neighbour in closed_list and closed_list[neighbour] is True:
                        closed_list[neighbour] = False
                        open_list.add((end - neighbour + path_to_neighbour_cost, neighbour))
                        open_list_check[neighbour] = True

            open_list.pop(0)
            open_list_check[current] = False
            closed_list[current] = True

        if path_found:
            path: [Hex] = []
            while end is not None:
                path.append(end)
                end = parent[end]
            path.reverse()
            return path
        else:
            return None

    def is_valid(self, target_hex: Hex) -> bool:
        """
        Checks if hex is valid for the current map
        :param target_hex:
        :return: True if valid, False otherwise
        """
        coords = target_hex.get_coords()
        if sum(coords) != 0:
            return False

        return not any(coords[i] >= self.__map_size or coords[i] <= -self.__map_size for i in range(3))

    def is_tank_in_base(self, tank_id: int) -> bool:
        return tank_id in self.__tanks_in_base

    def get_tank_position(self, tank_id: int) -> Hex:
        return self.__tanks[tank_id].get_pos()

    def set_tanks(self, tanks: dict[int: Tank]):
        # Tanks set from Game
        self.__tanks = tanks
        for tank_id, tank in tanks.items():
            spawn_position = tank.get_spawn_pos()
            self.__entities[spawn_position] = tank

    def tank_in_pos(self, pos: Hex) -> Tank:
        for tank_id, tank in self.__tanks.items():
            if tank.get_pos() == pos:
                return tank

    def get_base(self):
        return self.__base
