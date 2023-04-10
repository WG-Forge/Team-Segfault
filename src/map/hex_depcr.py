from math import sqrt

sqrt3 = sqrt(3)


class HexDepcr:
    """Class that represents one Hex"""

    def __init__(self, args: [int]):
        self.__x, self.__y, self.__z = args

    def get_coord(self) -> tuple[int, int, int]:
        return self.__x, self.__y, self.__z

    @staticmethod
    def get_center(coord: tuple):
        """Returns the center of a given hex in cartesian co-ordinates"""
        x, y, z = coord
        return (1 * x - 0.5 * y - 0.5 * z), (sqrt3 / 2 * y - sqrt3 / 2 * z)

    @staticmethod
    def get_corners(coord: tuple) -> tuple:
        # Returns cartesian coordinates of the six corners for a given array of hex coordinates + the first one twice
        x, y, z = coord
        first = Hex.make_center((x, y, z - 1))
        return (
            first,
            Hex.make_center((x, y + 1, z)),
            Hex.make_center((x - 1, y, z)),
            Hex.make_center((x, y, z + 1)),
            Hex.make_center((x, y - 1, z)),
            Hex.make_center((x + 1, y, z)),
            first
        )

    def __add__(self, other):
        return Hex([fst + snd for fst, snd in zip(self.get_coord(), other.get_coord())])

    def __neg__(self):
        return Hex([-self.__x, -self.__y, -self.__z])

    def __eq__(self, other):
        return self.get_coord() == other.get_coord()

    def __lt__(self, other):
        return self.get_coord() < self.get_coord()

    # calculates the distance between 2 hexes
    def __sub__(self, other) -> int:
        x, y, z = other.get_coord()
        return (abs(self.__x - x) + abs(self.__y - y) + abs(self.__z - z)) / 2

    def __str__(self):
        return f'x:{self.__x}, y:{self.__y}, z:{self.__z}'

    def __hash__(self):
        return hash(tuple(self.get_coord()))
