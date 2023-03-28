class Hex:
    """Class that represents one Hex"""

    def __init__(self, args: list):
        self.__x = args[0]
        self.__y = args[1]
        self.__z = args[2]

    def get_coordinates(self) -> list[int]:
        return [self.__x, self.__y, self.__z]

    def __add__(self, other):
        return Hex([fst + snd for fst, snd in zip(self.get_coordinates(), other.get_coordinates())])

    def __neg__(self):
        return Hex([-self.__x, -self.__y, -self.__z])

    def __eq__(self, other):
        return self.get_coordinates() == other.get_coordinates()

    def __str__(self):
        return f'x:{self.__x}, y:{self.__y}, z:{self.__z}'

    def __hash__(self):
        return hash(tuple(self.get_coordinates()))
