from game.entity.map_features.spawn import Spawn
from game.entity.tanks.tank import Tank
from game.entity.tanks.types.artillery import Artillery
from game.entity.tanks.types.destroyer import TankDestroyer
from game.entity.tanks.types.heavy import HeavyTank
from game.entity.tanks.types.light import LightTank
from game.entity.tanks.types.medium import MediumTank


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
