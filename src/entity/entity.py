class Entity:

    def __init__(self, name: str):
        self.__type = name

    def draw(self) -> None:
        pass

    def update(self, hp: str, capture_pts: str):
        pass

    def get_type(self) -> str:
        return self.__type
