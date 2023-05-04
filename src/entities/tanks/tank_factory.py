from src.entities.entity_enum import Entities
from src.entities.map_features.landmarks.spawn import Spawn
from src.entities.tanks.tank import Tank
from src.entities.tanks.types.artillery import Artillery
from src.entities.tanks.types.destroyer import TankDestroyer
from src.entities.tanks.types.heavy import HeavyTank
from src.entities.tanks.types.light import LightTank
from src.entities.tanks.types.medium import MediumTank


class TankFactory:
    TANK_TYPES = {
        Entities.LIGHT_TANK: LightTank,
        Entities.MEDIUM_TANK: MediumTank,
        Entities.HEAVY_TANK: HeavyTank,
        Entities.TANK_DESTROYER: TankDestroyer,
        Entities.ARTILLERY: Artillery
    }

    def __init__(self, vehicles: dict, active_players: dict, game_map: dict, catapult_coords: tuple):
        self.__tanks: dict[int, Tank] = self.__make_tanks(vehicles, active_players, game_map, catapult_coords)

    @staticmethod
    def __make_tanks(vehicles: dict, active_players: dict,
                     game_map: dict, catapult_coords: tuple) -> dict[int, Tank]:
        tanks: dict[int, Tank] = {}
        for vehicle_id, vehicle_info in vehicles.items():
            player = active_players[vehicle_info["player_id"]]
            tank, spawn = TankFactory.make_tank_and_spawn(int(vehicle_id), vehicle_info, player.color,
                                                          player.index, catapult_coords)
            game_map[tank.coord]['tank'] = tank
            game_map[tank.spawn_coord]['feature'] = spawn
            tanks[int(vehicle_id)] = tank
            player.add_tank(tank)
        return tanks

    @staticmethod
    def make_tank_and_spawn(tank_id: int, tank_info: dict, tank_color: tuple,
                            player_index: int, catapult_coords: tuple) -> tuple[TANK_TYPES, Spawn]:
        tank_class = TankFactory.TANK_TYPES[tank_info["vehicle_type"]]
        tank = tank_class(tank_id, tank_info, tank_color, player_index, catapult_coords)
        spawn = Spawn(tank.spawn_coord, tank_id, tank_color)
        return tank, spawn

    @property
    def tanks(self) -> dict[int, Tank]: return self.__tanks
