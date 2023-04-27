from .feature import Feature


class Spawn(Feature):
    def __init__(self, coord: tuple, tank_id: int = -1):
        self.__belongs_to = tank_id
        super().__init__('spawn', coord)

    def get_belongs_id(self) -> int:
        return self.__belongs_to
