from typing import Dict, Tuple

from entities.entity_enum import Entities
from entities.map_features.Landmarks.spawn import Spawn
from entities.tanks.types.artillery import Artillery
from entities.tanks.types.destroyer import TankDestroyer
from entities.tanks.types.heavy import HeavyTank
from entities.tanks.types.light import LightTank
from entities.tanks.types.medium import MediumTank
from tank import Tank


class TankFactory:
    TANK_TYPES = {
        Entities.LIGHT_TANK: LightTank,
        Entities.MEDIUM_TANK: MediumTank,
        Entities.HEAVY_TANK: HeavyTank,
        Entities.TANK_DESTROYER: TankDestroyer,
        Entities.ARTILLERY: Artillery
    }

    def __init__(self, vehicles: Dict, active_players: Dict, game_map: Dict, catapult_coords: Tuple):
        self.__tanks: Dict[int, Tank] = self.__make_tanks(vehicles, active_players, game_map, catapult_coords)

    def __make_tanks(self, vehicles: Dict, active_players: Dict,
                     game_map: Dict, catapult_coords: Tuple) -> Dict[int, Tank]:
        tanks: Dict[int, Tank] = {}
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
    def make_tank_and_spawn(tank_id: int, tank_info: Dict, tank_color: Tuple,
                            player_index: int, catapult_coords: Tuple) -> Tuple:
        tank_class = TankFactory.TANK_TYPES[tank_info["vehicle_type"]]
        tank = tank_class(tank_id, tank_info, tank_color, player_index, catapult_coords)
        spawn = Spawn(tank.spawn_coord, tank_id, tank_color)
        return tank, spawn

    @property
    def tanks(self) -> Dict[int, Tank]: return self.__tanks
