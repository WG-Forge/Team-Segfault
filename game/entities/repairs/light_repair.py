from entities.entity import Entities
from entities.repairs.repair import Repair


class LightRepair(Repair):

    def __init__(self):
        super().__init__(Entities.LIGHT_REPAIR)
