from abc import ABC

from src.entity.tanks.tank import Tank


class MediumTank(Tank, ABC):
    def __init__(self, tank_id: int, tank_info: dict):
        self.__sp: int = 2  # Speed Points
        self.__dp: int = 2  # Destruction Points
        super().__init__(tank_id, tank_info)
