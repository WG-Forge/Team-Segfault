from entity.tanks.tank import Tank
from entity.tanks.artillery import Artillery
from entity.tanks.destoryer import TankDestroyer
from entity.tanks.heavy import HeavyTank
from entity.tanks.light import LightTank
from entity.tanks.medium import MediumTank


class TankMaker:
    TANK_TYPES = {
        "light_tank": LightTank,
        "medium_tank": MediumTank,
        "heavy_tank": HeavyTank,
        "at_spg": TankDestroyer,
        "spg": Artillery
    }

    @classmethod
    def create_tank(cls, tank_id: int, tank_info: dict) -> Tank:
        tank_type = tank_info["vehicle_type"]
        tank_class = cls.TANK_TYPES[tank_type]
        tank = tank_class(tank_id, tank_info)
        return tank
