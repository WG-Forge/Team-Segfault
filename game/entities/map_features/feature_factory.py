from typing import Dict, List, Tuple

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

    def __init__(self, features: Dict, game_map: Dict):
        self.__base_coords: List[Tuple] = []
        self.__base_adjacent_coords: List[Tuple] = []
        self.__catapult_coords: List[Tuple] = []
        self.__make_features(features, game_map)

    def __make_features(self, features: Dict, game_map: Dict) -> None:
        for name, coords in features.items():
            features_class = self.FEATURE_TYPES.get(name)
            if not features_class:
                print(f"Support for {name} needed")
                continue
            for d in coords:
                coord: Tuple = (d['x'], d['y'], d['z'])
                game_map[coord]['feature'] = features_class(coord)
                if name == Entities.BASE:
                    self.__base_coords.append(coord)
                elif name == Entities.CATAPULT:
                    self.__catapult_coords.append(coord)
            if name == Entities.BASE:
                self.__make_base_adjacents()

    def __make_base_adjacents(self) -> None:
        adjacent_deltas = Hex.make_ring(1)
        self.__base_adjacent_coords = {
                                          Hex.coord_sum(delta, base_coord)
                                          for base_coord in self.__base_coords
                                          for delta in adjacent_deltas
                                      } - set(self.__base_coords)

    @property
    def catapult_coords(self) -> Tuple[Tuple, ...]:
        return tuple(self.__catapult_coords)

    @property
    def base_coords(self) -> Tuple[Tuple, ...]:
        return tuple(self.__base_coords)

    @property
    def base_adjacents(self) -> Tuple[Tuple, ...]:
        return tuple(self.__base_adjacent_coords)
