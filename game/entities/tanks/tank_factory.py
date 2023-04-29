from entities.map_features.spawn import Spawn
from entities.tanks.types.artillery import Artillery
from entities.tanks.types.destroyer import TankDestroyer
from entities.tanks.types.heavy import HeavyTank
from entities.tanks.types.light import LightTank
from entities.tanks.types.medium import MediumTank


class TankFactory:
    TANK_TYPES = {
        "light_tank": LightTank,
        "medium_tank": MediumTank,
        "heavy_tank": HeavyTank,
        "at_spg": TankDestroyer,
        "spg": Artillery
    }

    @staticmethod
    def create_tank_and_spawn(tank_id: int, tank_info: dict, tank_color, player_index: int) -> tuple:
        tank_class = TankFactory.TANK_TYPES[tank_info["vehicle_type"]]
        tank = tank_class(tank_id, tank_info, tank_color, player_index)
        spawn = Spawn(tank.get_spawn_coord(), tank_id, tank_color)
        return tank, spawn
