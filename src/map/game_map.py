import json

import matplotlib.pyplot as plt

from hex import Hex
from src.entity.entity import Entity
from src.entity.tank import Tank


class GameMap:
    def __init__(self, game_map: str):
        self.__size: int = 0
        self.__entities: dict[Hex, Entity] = {}
        # tank_id -> hex
        self.__tanks: dict[int, Hex] = {}
        self.__tanks_in_base: list[Tank] = []
        self.parse_map(game_map)

    def parse_map(self, game_map: str) -> None:
        game_map = json.loads(game_map)
        self.__size = game_map["size"]
        for entity, coordinates in game_map["content"].items():
            for coordinate in coordinates:
                h = Hex([coordinate["x"], coordinate["y"], coordinate["z"]])
                self.__entities[h] = Entity(entity)

    def update(self, game_state: str) -> None:
        game_state = json.loads(game_state)
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
                print(vehicle_info)
                self.__entities[new_position] = Tank(vehicle_id, vehicle_info)

    def draw_map(self) -> None:
        # TODO: optimize, since special hexes are drawn twice and adjacent hexes have some same edges
        plt.figure()
        # draw the whole map
        for x in range(-self.__size, self.__size + 1):
            for y in range(-self.__size, self.__size + 1):
                for z in range(-self.__size, self.__size + 1):
                    if x + y + z == 0:
                        coords = Hex.hex_corners([x, y, z])
                        coords.append(coords[0])
                        xs, ys = zip(*coords)
                        plt.plot(xs, ys, 'k')
        # draw special hexes
        for h, entity in self.__entities.items():
            coords = Hex.hex_corners(h.get_coordinates())
            coords.append(coords[0])
            xs, ys = zip(*coords)
            # default obstacle
            color = "r"
            if entity.get_type() == "base":
                color = "g"
            plt.plot(xs, ys, color)
        plt.axis('off')
        plt.show()

    def set_entity(self, hex_coord: Hex, entity: Entity) -> None:
        self.__entities[hex_coord] += entity

    def get_tank_position(self, tank_id: int) -> Hex:
        return self.__tanks[tank_id]

    def get_entities(self) -> dict[Hex, Entity]:
        return self.__entities


if __name__ == '__main__':
    with open('../../map.json') as f:
        gm = GameMap(f.read())
        d = gm.get_entities()
        for k, v in d.items():
            print(f'hex: {k}; entity: {v.get_type()}')

        with open("../../game_state.json") as f1:
            gm.update(f1.read())
            d = gm.get_entities()
            for k, v in d.items():
                print(f'hex: {k}; entity: {v.get_type()}')

            gm.draw_map()
