from entities.entity_enum import Entities
from entities.map_features.bonuses.catapult import Catapult
from entities.map_features.bonuses.hard_repair import HardRepair
from entities.map_features.bonuses.light_repair import LightRepair
from entities.map_features.landmarks.base import Base
from entities.map_features.landmarks.empty import Empty
from entities.map_features.landmarks.obstacle import Obstacle
from game_map.hex import Hex


class FeatureFactory:
    FEATURE_TYPES = {
        Entities.EMPTY: Empty,
        Entities.OBSTACLE: Obstacle,
        Entities.BASE: Base,
        Entities.LIGHT_REPAIR: LightRepair,
        Entities.HARD_REPAIR: HardRepair,
        Entities.CATAPULT: Catapult,
    }

    def __init__(self, features: dict, game_map: dict):
        self.__base_coords: list[tuple] = []
        self.__base_adjacent_coords: list[tuple] = []
        self.__catapult_coords: list[tuple] = []
        self.__hard_repair_coords: list[tuple] = []
        self.__light_repair_coords: list[tuple] = []
        self.__make_features(features, game_map)

    def __make_features(self, features: dict, game_map: dict) -> None:
        feature_coords = {Entities.BASE: [], Entities.CATAPULT: [], Entities.LIGHT_REPAIR: [], Entities.HARD_REPAIR: []}

        for name, coords in features.items():
            feature_class = self.FEATURE_TYPES.get(name)
            if not feature_class:
                print(f"Support for {name} needed")
                continue

            coord_list = feature_coords.get(name)
            for d in coords:
                coord = (d['x'], d['y'], d['z'])
                game_map[coord]['feature'] = feature_class(coord)
                if coord_list:
                    coord_list.append(coord)

        self.__base_coords = feature_coords[Entities.BASE]
        self.__catapult_coords = feature_coords[Entities.CATAPULT]
        self.__light_repair_coords = feature_coords[Entities.LIGHT_REPAIR]
        self.__hard_repair_coords = feature_coords[Entities.HARD_REPAIR]

        self.__make_base_adjacents()

    def __make_base_adjacents(self) -> None:
        adjacent_deltas = Hex.make_ring(1)
        self.__base_adjacent_coords = {
                                          Hex.coord_sum(delta, base_coord)
                                          for base_coord in self.__base_coords
                                          for delta in adjacent_deltas
                                      } - set(self.__base_coords)

    @property
    def light_repair_coords(self) -> tuple[tuple, ...]:
        return tuple(self.__light_repair_coords)

    @property
    def hard_repair_coords(self) -> tuple[tuple, ...]:
        return tuple(self.__hard_repair_coords)

    @property
    def catapult_coords(self) -> tuple[tuple, ...]:
        return tuple(self.__catapult_coords)

    @property
    def base_coords(self) -> tuple[tuple, ...]:
        return tuple(self.__base_coords)

    @property
    def base_adjacents(self) -> tuple[tuple, ...]:
        return tuple(self.__base_adjacent_coords)
