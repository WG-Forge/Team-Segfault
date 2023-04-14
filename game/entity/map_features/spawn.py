from abc import ABC

from game.entity.map_features.feature import Feature


class Spawn(Feature, ABC):
    color = 'magenta'

    def __init__(self, coord: tuple, tank_id: int):
        self.__belongs_to = tank_id
        super().__init__('spawn', coord, Spawn.color)

    def get_belongs_id(self) -> int:
        return self.__belongs_to
