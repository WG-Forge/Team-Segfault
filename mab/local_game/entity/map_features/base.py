from .feature import Feature


class Base(Feature):
    def __init__(self, coord: tuple):
        super().__init__('base', coord)