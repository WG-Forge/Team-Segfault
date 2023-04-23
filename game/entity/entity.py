class Entity:
    def __init__(self, name: str):
        self._type: str = name

    def get_type(self) -> str:
        return self._type

    @staticmethod
    def set_radii(num_of_radii: int):
        Entity._num_of_radii = num_of_radii
