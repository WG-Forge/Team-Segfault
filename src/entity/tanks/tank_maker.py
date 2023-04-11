from entity.map_features.spawn import Spawn
from entity.tanks.tank import Tank
from entity.tanks.types.artillery import Artillery
from entity.tanks.types.destoryer import TankDestroyer
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
    def create_tank(tank_id: int, tank_info: dict, tank_colour: str, player_index: int) -> tuple[Tank, Spawn]:
        tank_class = TankMaker.TANK_TYPES[tank_info["vehicle_type"]]
        tank = tank_class(tank_id, tank_info, tank_colour, player_index)
        spawn = Spawn(tank.get_coord(), tank_id)
        return tank, spawn
