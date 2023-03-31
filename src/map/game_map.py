import matplotlib.pyplot as plt

from src.entity.entity import Entity
from src.entity.tank import Tank
from src.map.hex import Hex


class GameMap:
    def __init__(self, game_map: dict):
        self.__map_size: int = 0
        self.__entities: dict[Hex, Entity] = {}
        # tank_id -> hex
        self.__tanks: dict[int, Hex] = {}
        self.__tanks_in_base: list[Tank] = []
        self.parse_map(game_map)

    def parse_map(self, game_map: dict) -> None:
        self.__map_size = game_map["size"]
        for entity, coordinates in game_map["content"].items():
            for coordinate in coordinates:
                h = Hex([coordinate["x"], coordinate["y"], coordinate["z"]])
                self.__entities[h] = Entity(entity)

    def update(self, game_state: dict) -> None:
        vehicles = game_state["vehicles"]
        for vehicle_id, vehicle_info in vehicles.items():
            vehicle_id = int(vehicle_id)
            new_position = Hex([vehicle_info["position"]["x"],
                                vehicle_info["position"]["y"],
                                vehicle_info["position"]["z"]])

            if vehicle_id in self.__tanks:
                old_position = self.__tanks[vehicle_id]
                if old_position == new_position:
                    # this tank did not move, only update hp and capture points
                    self.__entities[new_position].update(vehicle_info["health"], vehicle_info["capture_points"])
                else:
                    # this tank did move -> update its position and after that update its hp and capture points
                    tank = self.__entities[old_position]
                    del self.__entities[old_position]
                    if self.__entities[new_position].get_type() == "base":
                        # tank moved to the base, append it to tanks_in_base list
                        self.__tanks_in_base.append(tank)
                    else:
                        # if light or hard repair was there, overwrite hex with this tank and
                        # update tank vehicle_info from server response
                        self.__entities[new_position] = tank

                    tank.update(vehicle_info["health"], vehicle_info["capture_points"])
                    self.__tanks[vehicle_id] = new_position
            else:
                # first occurrence; add this tank to entities and tanks hash map
                self.__tanks[vehicle_id] = new_position
                # add tank to list, since
                # print(vehicle_info)
                self.__entities[new_position] = Tank(vehicle_id, vehicle_info)

    def draw_map(self) -> None:
        # TODO: optimize, since special hexes are drawn twice and adjacent hexes have some same edges
        plt.figure()
        # draw the whole map
        for x in range(-self.__map_size, self.__map_size + 1):
            for y in range(-self.__map_size, self.__map_size + 1):
                z = -x - y
                if self.__map_size >= z >= -self.__map_size:
                    coords = Hex.get_corners([x, y, z])
                    coords.append(coords[0])
                    xs, ys = zip(*coords)
                    plt.plot(xs, ys, 'k')
        # draw entities
        for h, entity in self.__entities.items():
            color = "blue"
            if isinstance(entity, Tank):
                tank_dot = Hex.get_center(h.get_coordinates())
                plt.plot(tank_dot[0], tank_dot[1], marker='o', markersize='6', markerfacecolor=color)
                continue

            entity_type = entity.get_type()
            if entity_type == "base":
                color = "g"
            elif entity_type == "obstacle":
                color = "r"
            coords = Hex.get_corners(h.get_coordinates())
            coords.append(coords[0])
            xs, ys = zip(*coords)
            plt.plot(xs, ys, color)

        plt.axis('off')
        plt.show()

    def set_entity(self, hex_coord: Hex, entity: Entity) -> None:
        self.__entities[hex_coord] += entity

    def get_tank_position(self, tank_id: int) -> Hex:
        return self.__tanks[tank_id]

    def get_entities(self) -> dict:
        return self.__entities
