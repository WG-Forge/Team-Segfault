from abc import abstractmethod

# TODO: Implement obstacles as entities
from pygame import Surface


class Entity:
    def __init__(self, name: str):
        self._type: str = name

    @abstractmethod
    def draw(self, screen: Surface) -> None:
        pass

    @abstractmethod
    def update(self, hp: str, capture_pts: str):
        pass

    @abstractmethod
    def get_type(self) -> str:
        return self._type

    @staticmethod
    def set_radii(num_of_radii: int):
        Entity._num_of_radii = num_of_radii
