from .feature import Feature


class Empty(Feature):

    def __init__(self, coord: tuple):
        super().__init__('empty', coord)
