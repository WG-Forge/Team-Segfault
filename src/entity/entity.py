from abc import abstractmethod


class Entity:

    def __init__(self, name: str, is_tank: bool = True):
        self._type: str = name
        self.__is_tank: bool = is_tank

    @abstractmethod
    def draw(self) -> None:
        pass

    @abstractmethod
    def update(self, hp: str, capture_pts: str):
        pass

    @abstractmethod
    def get_type(self) -> str:
        return self._type

    def is_tank(self) -> bool:
        return self.__is_tank
