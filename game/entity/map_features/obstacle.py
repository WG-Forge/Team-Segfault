from entity.map_features.feature import Feature


class Obstacle(Feature):
    __color: tuple = (51, 46, 46)  # dark red

    def __init__(self, coord: tuple):
        super().__init__('obstacle', coord)

    def get_color(self) -> tuple:
        return Obstacle.__color
