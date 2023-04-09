from abc import abstractmethod

from map.hex import Hex


# TODO: Implement obstacles as entities
class Entity:
    def __init__(self, name: str):
        self._type: str = name

    @abstractmethod
    def draw(self) -> None:
        pass

    @abstractmethod
    def update(self, hp: str, capture_pts: str):
        pass

    @abstractmethod
    def get_type(self) -> str:
        return self._type
