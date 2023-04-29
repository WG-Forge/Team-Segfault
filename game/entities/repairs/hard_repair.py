from entities.entity import Entities
from entities.repairs.repair import Repair


class HardRepair(Repair):

    def __init__(self):
        super().__init__(Entities.HARD_REPAIR)
