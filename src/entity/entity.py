from abc import abstractmethod


class Entity:

    def __init__(self, name: str):
        self._type = name

    @abstractmethod
    def draw(self) -> None:
        pass

    @abstractmethod
    def update(self, hp: str, capture_pts: str):
        pass

    @abstractmethod
    def get_type(self) -> str:
        return self._type
