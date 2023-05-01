from abc import abstractmethod

from entities.entity_enum import Entities
from entities.map_features.feature import Feature


class Bonus(Feature):
    def __init__(self, name: str, coord: tuple, color: str):
        super().__init__(Entities(name), coord, color)

    @abstractmethod
    def is_usable(self) -> bool:
        pass

    @abstractmethod
    def was_used(self) -> None:
        print('No need to call this method for non catapult bonuses')
