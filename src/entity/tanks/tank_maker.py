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

    @classmethod
    def create_tank(cls, tank_id: int, tank_info: dict, tank_colour: str) -> Tank:
        tank_class = cls.TANK_TYPES[tank_info["vehicle_type"]]
        tank = tank_class(tank_id, tank_info, tank_colour)
        return tank
