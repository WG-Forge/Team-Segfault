from math import sqrt

sqrt3 = sqrt(3)


class Hex:
    """Class that represents one Hex"""

    def __init__(self, args: list):
        self.__x = args[0]
        self.__y = args[1]
        self.__z = args[2]

    def get_coordinates(self) -> list[int]:
        return [self.__x, self.__y, self.__z]

    @staticmethod
    def get_center(coordinates: list[3]):
        """Returns the center of a given hex in cartesian co-ordinates"""
        x = coordinates[0]
        y = coordinates[1]
        z = coordinates[2]
        return [(1 * x - 0.5 * y - 0.5 * z),
                (sqrt3 / 2 * y - sqrt3 / 2 * z)]

    @staticmethod
    def get_corners(coordinates: list[3]) -> list[6]:
        """Returns cartesian coordinates of the six corners for a given array of hex coordinates"""
        x = coordinates[0]
        y = coordinates[1]
        z = coordinates[2]
        return [
            Hex.get_center([x, y, z - 1]),
            Hex.get_center([x, y + 1, z]),
            Hex.get_center([x - 1, y, z]),
            Hex.get_center([x, y, z + 1]),
            Hex.get_center([x, y - 1, z]),
            Hex.get_center([x + 1, y, z])
        ]

    def __add__(self, other):
        return Hex([fst + snd for fst, snd in zip(self.get_coordinates(), other.get_coordinates())])

    def __neg__(self):
        return Hex([-self.__x, -self.__y, -self.__z])

    def __eq__(self, other):
        return self.get_coordinates() == other.get_coordinates()

    # calculates the distance between 2 hexes
    def __sub__(self, other):
        other_coords = other.get_coordinates()
        return (abs(self.__x - other_coords[0]) +
                abs(self.__y - other_coords[1]) +
                abs(self.__z - other_coords[2])) / 2

    def __str__(self):
        return f'x:{self.__x}, y:{self.__y}, z:{self.__z}'

    def __hash__(self):
        return hash(tuple(self.get_coordinates()))
