from src.entity.tanks.tank import Tank
from src.entity.tanks.artillery import Artillery
from src.entity.tanks.destoryer import TankDestroyer
from src.entity.tanks.heavy import HeavyTank
from src.entity.tanks.light import LightTank
from src.entity.tanks.medium import MediumTank


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
