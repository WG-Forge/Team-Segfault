from collections import defaultdict

import matplotlib.pyplot as plt
from sortedcontainers import SortedSet

from src.client.server_enum import Action
from src.entity.entity import Entity
from src.entity.tanks.tank import Tank
from src.map.hex import Hex


class GameMap:
    def __init__(self, game_map: dict):
        self.__map_size: int = 0
        self.__entities: dict[Hex, Entity] = {}
        # tank_id -> hex
        self.__tank_positions: dict[int, Hex] = {}
        self.__tanks: dict[int, Tank] = {}
        # tanks_in_base could probably be deleted
        self.__tanks_in_base: list[int] = []
        self.__base: [Hex] = []
        self.parse_map(game_map)

    def parse_map(self, game_map: dict) -> None:
        """
        Saves entity data
        :param game_map: dict of GAME_MAP response
        :return: None
        """
        self.__map_size = game_map["size"]
        for entity, coordinates in game_map["content"].items():
            for coordinate in coordinates:
                h = Hex([coordinate["x"], coordinate["y"], coordinate["z"]])
                if entity == "base":
                    self.__base.append(h)
                else:
                    self.__entities[h] = Entity(entity)

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
                new_position = Hex([data['target']['x'], data['target']['y'], data['target']['z']])

                tank = self.__tanks[tank_id]
                if action["action_type"] == Action.MOVE:
                    # if tank was in base before movement, remove it from tanks_in_base
                    if self.__tank_positions[tank_id] in self.__base:
                        self.__tanks_in_base.remove(tank_id)

                    self.__entities[new_position] = tank
                    del self.__entities[self.__tank_positions[tank_id]]
                    self.__tank_positions[tank_id] = new_position

                    if new_position in self.__base:
                        self.__tanks_in_base.append(tank_id)

                if action["action_type"] == Action.SHOOT:
                    tank: Tank = self.__entities[new_position]
                    if tank.reduce_hp():
                        spawn = tank.get_spawn_coordinate()
                        del self.__entities[new_position]
                        self.__entities[spawn] = tank
                        self.__tank_positions[tank.get_id()] = spawn
            return

        vehicles = game_state["vehicles"]
        for vehicle_id, vehicle_info in vehicles.items():
            vehicle_id = int(vehicle_id)
            new_position = Hex([vehicle_info["position"]["x"],
                                vehicle_info["position"]["y"],
                                vehicle_info["position"]["z"]])

            if vehicle_id in self.__tank_positions:
                old_position = self.__tank_positions[vehicle_id]
                if old_position == new_position:
                    # this tank did not move, only update hp and capture points
                    self.__entities[new_position].update(vehicle_info["health"], vehicle_info["capture_points"])
                else:
                    # this tank did move -> update its position and after that update its hp and capture points
                    tank = self.__entities[old_position]
                    if old_position in self.__base:
                        self.__tanks_in_base.remove(tank.get_id())

                    del self.__entities[old_position]
                    if new_position in self.__base:
                        # tank moved to the base, append it to tanks_in_base list
                        self.__tanks_in_base.append(tank.get_id())

                    # if light or hard repair was there, overwrite hex with this tank and
                    # update tank vehicle_info from server response
                    self.__entities[new_position] = tank

                    tank.update(vehicle_info["health"], vehicle_info["capture_points"])
                    self.__tank_positions[vehicle_id] = new_position

            else:
                # first occurrence; add this tank to entities and tanks hash map
                self.__tank_positions[vehicle_id] = new_position
                tank = Tank(vehicle_id, vehicle_info)
                self.__entities[new_position] = tank
                self.__tanks[vehicle_id] = tank

    def draw_map(self) -> None:
        # TODO: optimize, since special hexes are drawn twice and adjacent hexes have some same edges
        plt.figure()
        # draw the whole map
        for x in range(-self.__map_size + 1, self.__map_size):
            for y in range(-self.__map_size + 1, self.__map_size):
                z = -x - y
                if self.__map_size > z > -self.__map_size:
                    coords = Hex.get_corners([x, y, z])
                    coords.append(coords[0])
                    xs, ys = zip(*coords)
                    plt.plot(xs, ys, 'k')

        # draw base
        for h in self.__base:
            coords = Hex.get_corners(h.get_coordinates())
            coords.append(coords[0])
            xs, ys = zip(*coords)
            plt.plot(xs, ys, 'g')

        # draw entities
        marker = 'o'
        for h, entity in self.__entities.items():
            color = "blue"
            if isinstance(entity, Tank):
                marker = entity.get_drawing_symbol()
                tank_dot = Hex.get_center(h.get_coordinates())
                plt.plot(tank_dot[0], tank_dot[1], marker=marker, markersize='6',
                         markerfacecolor=color, markeredgewidth=0.0)
                continue

            entity_type = entity.get_type()
            if entity_type == "obstacle":
                color = "r"
            coords = Hex.get_corners(h.get_coordinates())
            coords.append(coords[0])
            xs, ys = zip(*coords)
            plt.plot(xs, ys, color)

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
                if not self.is_valid(neighbour) or \
                        (neighbour in self.__entities and self.__entities[neighbour].get_type() == 'obstacle'):
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
        coords = target_hex.get_coordinates()
        if sum(coords) != 0:
            return False

        return not any(coords[i] >= self.__map_size or coords[i] <= -self.__map_size for i in range(3))

    def is_tank_in_base(self, tank_id: int) -> bool:
        return tank_id in self.__tanks_in_base

    def set_entity(self, hex_coord: Hex, entity: Entity) -> None:
        self.__entities[hex_coord] += entity

    def get_tank_position(self, tank_id: int) -> Hex:
        return self.__tank_positions[tank_id]

    def get_entities(self) -> dict:
        return self.__entities

    def get_base(self) -> [Hex]:
        return self.__base

    def get_entity_at(self, hex_pos: Hex):
        if hex_pos in self.__entities:
            return self.__entities[hex_pos]
        return None
