from .tank import Tank
from .types.artillery import Artillery
from .types.destroyer import TankDestroyer
from .types.heavy import HeavyTank
from .types.light import LightTank
from .types.medium import MediumTank
from ..map_features.spawn import Spawn


class TankMaker:
    TANK_TYPES = {
        "light_tank": LightTank,
        "medium_tank": MediumTank,
        "heavy_tank": HeavyTank,
        "at_spg": TankDestroyer,
        "spg": Artillery
    }

    @staticmethod
    def create_tank(tank_id: int, tank_info: dict, tank_colour: str, player_index: int) -> tuple[Tank, Spawn]:
        tank_class = TankMaker.TANK_TYPES[tank_info["vehicle_type"]]
        tank = tank_class(tank_id, tank_info, tank_colour, player_index)
        spawn = Spawn(tank.get_coord(), tank_id)
        return tank, spawn
