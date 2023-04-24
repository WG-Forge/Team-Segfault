from entity.map_features.spawn import Spawn
from entity.tanks.types.artillery import Artillery
from entity.tanks.types.destroyer import TankDestroyer
from entity.tanks.types.heavy import HeavyTank
from entity.tanks.types.light import LightTank
from entity.tanks.types.medium import MediumTank


class TankMaker:
    TANK_TYPES = {
        "light_tank": LightTank,
        "medium_tank": MediumTank,
        "heavy_tank": HeavyTank,
        "at_spg": TankDestroyer,
        "spg": Artillery
    }

    @staticmethod
    def create_tank_and_spawn(tank_id: int, tank_info: dict, tank_color, player_index: int) -> tuple:
        tank_class = TankMaker.TANK_TYPES[tank_info["vehicle_type"]]
        tank = tank_class(tank_id, tank_info, tank_color, player_index)
        spawn = Spawn(tank.get_coord(), tank_id, tank_color)
        return tank, spawn
