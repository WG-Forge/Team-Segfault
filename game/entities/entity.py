from abc import ABC


# Entity - Abstract Base Class
class Entity(ABC):
    def __init__(self, name: str):
        self._type: str = name

    def get_type(self) -> str:
        return self._type
