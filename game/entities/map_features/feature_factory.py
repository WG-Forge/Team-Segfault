from typing import Dict, List

from entities.entity_enum import Entities
from entities.map_features.bonuses.catapult import Catapult
from entities.map_features.bonuses.hard_repair import HardRepair
from entities.map_features.bonuses.light_repair import LightRepair
from entities.map_features.physical.base import Base
from entities.map_features.physical.empty import Empty
from entities.map_features.physical.obstacle import Obstacle
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

    def __init__(self, features: Dict, game_map: Dict):
        self.__map = game_map
        self.__base_coords = []
        self.__base_adjacent_coords = []
        self.__make_features(features)

    def __make_features(self, features: Dict):
        for name, coords in features.items():
            features_class = self.FEATURE_TYPES.get(name)
            if not features_class:
                print(f"Support for {name} needed")
                continue
            for d in coords:
                coord = (d['x'], d['y'], d['z'])
                self.__map[coord]['feature'] = features_class(coord)
                if name == Entities.BASE:
                    self.__base_coords.append(coord)
            if name == Entities.BASE:
                self.__make_base_adjacents()

    def __make_base_adjacents(self):
        adjacent_deltas = Hex.make_ring(1)
        self.__base_adjacent_coords = {Hex.coord_sum(delta, base_coord) for base_coord in self.__base_coords
                                       for delta in adjacent_deltas} - set(self.__base_coords)

    def get_base_coords(self):
        return tuple(self.__base_coords)

    def get_base_adjacents(self):
        return tuple(self.__base_adjacent_coords)

# end
