from entity.map_features.feature import Feature


class Spawn(Feature):
    __color: tuple = (135, 126, 126)  # dimmed magenta

    def __init__(self, coord: tuple, tank_id: int):
        self.__belongs_to = tank_id
        super().__init__('spawn', coord)

    def get_color(self) -> tuple:
        return Spawn.__color

    def get_belongs_id(self) -> int:
        return self.__belongs_to
