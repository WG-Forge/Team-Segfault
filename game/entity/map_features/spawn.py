from entity.map_features.feature import Feature


class Spawn(Feature):
    __color: tuple = (135, 126, 126)

    def __init__(self, coord: tuple, tank_id: int = -1, color: tuple = (135, 126, 126)):
        self.__belongs_to = tank_id
        super().__init__('spawn', coord, color)

    def get_belongs_id(self) -> int:
        return self.__belongs_to
