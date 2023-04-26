from entity.entity import Entity, Entities


class LightRepair(Entity):

    def __init__(self):
        super().__init__(Entities.LIGHT_REPAIR)
