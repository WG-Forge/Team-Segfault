from entities.map_features.spawn import Spawn
from entities.tanks.types.artillery import Artillery
from entities.tanks.types.destroyer import TankDestroyer
from entities.tanks.types.heavy import HeavyTank
from entities.tanks.types.light import LightTank
from entities.tanks.types.medium import MediumTank


class TankFactory:
    TANK_TYPES = {
        Entities.LIGHT_TANK: LightTank,
        Entities.MEDIUM_TANK: MediumTank,
        Entities.HEAVY_TANK: HeavyTank,
        Entities.TANK_DESTROYER: TankDestroyer,
        Entities.ARTILLERY: Artillery
    }

    @staticmethod
    def create_tank_and_spawn(tank_id: int, tank_info: dict, tank_color, player_index: int) -> tuple:
        tank_class = TankFactory.TANK_TYPES[tank_info["vehicle_type"]]
        tank = tank_class(tank_id, tank_info, tank_color, player_index)
        spawn = Spawn(tank.spawn_coord, tank_id, tank_color)
        return tank, spawn
