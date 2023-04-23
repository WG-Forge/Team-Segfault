from entity.map_features.feature import Feature


class Base(Feature):
    __color: tuple = (39, 161, 72)  # greenish

    def __init__(self, coord: tuple):
        super().__init__('base', coord, Base.__color)
