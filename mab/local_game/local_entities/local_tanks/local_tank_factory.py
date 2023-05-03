from local_entities.local_entity_enum import LocalEntities
from local_entities.local_map_features.local_landmarks.local_spawn import LocalSpawn
from local_entities.local_tanks.local_tank import LocalTank
from local_entities.local_tanks.local_types.local_artillery import LocalArtillery
from local_entities.local_tanks.local_types.local_destroyer import LocalTankDestroyer
from local_entities.local_tanks.local_types.local_heavy import LocalHeavyTank
from local_entities.local_tanks.local_types.local_light import LocalLightTank
from local_entities.local_tanks.local_types.local_medium import LocalMediumTank


class LocalTankFactory:
    TANK_TYPES = {
        LocalEntities.LIGHT_TANK: LocalLightTank,
        LocalEntities.MEDIUM_TANK: LocalMediumTank,
        LocalEntities.HEAVY_TANK: LocalHeavyTank,
        LocalEntities.TANK_DESTROYER: LocalTankDestroyer,
        LocalEntities.ARTILLERY: LocalArtillery
    }

    def __init__(self, vehicles: dict, active_players: dict, game_map: dict, catapult_coords: tuple):
        self.__tanks: dict[int, LocalTank] = self.__make_tanks(vehicles, active_players, game_map, catapult_coords)

    @staticmethod
    def __make_tanks(vehicles: dict, active_players: dict,
                     game_map: dict, catapult_coords: tuple) -> dict[int, LocalTank]:
        tanks: dict[int, LocalTank] = {}
        for vehicle_id, vehicle_info in vehicles.items():
            player = active_players[vehicle_info["player_id"]]
            tank, spawn = LocalTankFactory.make_tank_and_spawn(int(vehicle_id), vehicle_info, player.color,
                                                               player.index, catapult_coords)
            game_map[tank.coord]['tank'] = tank
            game_map[tank.spawn_coord]['feature'] = spawn
            tanks[int(vehicle_id)] = tank
            player.add_tank(tank)
        return tanks

    @staticmethod
    def make_tank_and_spawn(tank_id: int, tank_info: dict, tank_color: tuple,
                            player_index: int, catapult_coords: tuple) -> tuple[TANK_TYPES, LocalSpawn]:
        tank_class = LocalTankFactory.TANK_TYPES[tank_info["vehicle_type"]]
        tank = tank_class(tank_id, tank_info, tank_color, player_index, catapult_coords)
        spawn = LocalSpawn(tank.spawn_coord, tank_id, tank_color)
        return tank, spawn

    @property
    def tanks(self) -> dict[int, LocalTank]: return self.__tanks
