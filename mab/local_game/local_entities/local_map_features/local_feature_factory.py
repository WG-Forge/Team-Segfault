from local_entities.local_entity_enum import LocalEntities
from local_entities.local_map_features.local_bonuses.local_catapult import LocalCatapult
from local_entities.local_map_features.local_bonuses.local_hard_repair import LocalHardRepair
from local_entities.local_map_features.local_bonuses.local_light_repair import LocalLightRepair
from local_entities.local_map_features.local_landmarks.local_base import LocalBase
from local_entities.local_map_features.local_landmarks.local_empty import LocalEmpty
from local_entities.local_map_features.local_landmarks.local_obstacle import LocalObstacle
from local_map.local_hex import LocalHex


class LocalFeatureFactory:
    FEATURE_TYPES = {
        LocalEntities.EMPTY: LocalEmpty,
        LocalEntities.OBSTACLE: LocalObstacle,
        LocalEntities.BASE: LocalBase,
        LocalEntities.LIGHT_REPAIR: LocalLightRepair,
        LocalEntities.HARD_REPAIR: LocalHardRepair,
        LocalEntities.CATAPULT: LocalCatapult,
    }

    def __init__(self, features: dict, game_map: dict):
        self.__base_coords: list[tuple] = []
        self.__base_adjacent_coords: list[tuple] = []
        self.__catapult_coords: list[tuple] = []
        self.__hard_repair_coords: list[tuple] = []
        self.__light_repair_coords: list[tuple] = []
        self.__make_features(features, game_map)

    def __make_features(self, features: dict, game_map: dict) -> None:
        feature_coords = {LocalEntities.BASE: [], LocalEntities.CATAPULT: [], LocalEntities.LIGHT_REPAIR: [], LocalEntities.HARD_REPAIR: []}

        for name, coords in features.items():
            feature_class = self.FEATURE_TYPES.get(name)
            if not feature_class:
                print(f"Support for {name} needed")
                continue

            coords_list = []
            for d in coords:
                coord = (d['x'], d['y'], d['z'])
                game_map[coord]['feature'] = feature_class(coord)
                coords_list.append(coord)
            if name in feature_coords:
                feature_coords[name] = coords_list

        self.__base_coords = feature_coords[LocalEntities.BASE]
        self.__catapult_coords = feature_coords[LocalEntities.CATAPULT]
        self.__light_repair_coords = feature_coords[LocalEntities.LIGHT_REPAIR]
        self.__hard_repair_coords = feature_coords[LocalEntities.HARD_REPAIR]

        self.__make_base_adjacents()

    def __make_base_adjacents(self) -> None:
        adjacent_deltas = LocalHex.make_ring(1)
        self.__base_adjacent_coords = {
                                          LocalHex.coord_sum(delta, base_coord)
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
