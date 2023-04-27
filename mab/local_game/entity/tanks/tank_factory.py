from ..map_features.spawn import Spawn
from .types.artillery import Artillery
from .types.destroyer import TankDestroyer
from .types.heavy import HeavyTank
from .types.light import LightTank
from .types.medium import MediumTank


class TankFactory:
    TANK_TYPES = {
        "light_tank": LightTank,
        "medium_tank": MediumTank,
        "heavy_tank": HeavyTank,
        "at_spg": TankDestroyer,
        "spg": Artillery
    }

    @staticmethod
    def create_tank_and_spawn(tank_id: int, tank_info: dict, player_index: int) -> tuple:
        tank_class = TankFactory.TANK_TYPES[tank_info["vehicle_type"]]
        tank = tank_class(tank_id, tank_info, player_index)
        spawn = Spawn(tank.get_spawn_coord(), tank_id)
        return tank, spawn
