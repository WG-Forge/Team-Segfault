from entity.map_features.feature import Feature


class Empty(Feature):
    __color: tuple = (87, 81, 81)  # dark grey

    def __init__(self, coord: tuple):
        super().__init__('empty', coord, Empty.__color)
