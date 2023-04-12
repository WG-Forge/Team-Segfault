from math import sqrt


class Hex:
    __sqrt3 = sqrt(3)
    rings = []
    movements = ((1, 0, -1), (0, 1, -1), (1, -1, 0), (-1, 0, 1), (0, -1, 1), (-1, 1, 0))

    @staticmethod
    def make_rings():
        max_range = 3  # Change if maximum range of any tank is > 3 hexes
        Hex.rings = [Hex.make_ring(i) for i in range(1, max_range + 1)]

    @staticmethod
    def make_ring(ring_num: int) -> tuple[tuple[int, int, int]]:
        # Makes all the possible coordinates in a given ring around (0,0,0)
        ring_coords = []
        max_crd = ring_num
        min_crd = -ring_num
        required_abs_sum = ring_num * 2
        for i in range(min_crd, max_crd + 1):
            for j in range(max(min_crd, min_crd - i), min(max_crd, max_crd - i) + 1):
                k = -i - j
                if abs(i) + abs(j) + abs(k) == required_abs_sum:
                    ring_coords.append((i, j, k))
        return tuple(ring_coords)

    @staticmethod
    def make_directions(shot_len: int) -> tuple[tuple[int, int, int]]:
        """ used for finding TD shooting positions, not registering obstacles
        :param shot_len: length of a line
        :return: coordinates of straight lines in all 6 directions of length shot_len from (0,0,0)
        """
        direction_blocked: tuple = tuple(0 for _ in range(6))
        ret = [movement for movement in Hex.movements]
        for i in range(1, shot_len):
            for j in range(6):
                ret.append(Hex.coord_sum(ret[6 * (i - 1) + j], Hex.movements[j]))

        return tuple(ret)

    @staticmethod
    def manhattan_dist(coord1: tuple, coord2: tuple) -> int:
        x1, y1, z1 = coord1
        x2, y2, z2 = coord2
        return (abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)) // 2

    @staticmethod
    def coord_sum(coord1: tuple, coord2: tuple) -> tuple:
        return tuple(fst + snd for fst, snd in zip(coord1, coord2))

    @staticmethod
    def make_center(coord: tuple):
        """Returns the center of a given hex in cartesian co-ordinates"""
        x, y, z = coord
        return (1 * x - 0.5 * y - 0.5 * z), (Hex.__sqrt3 / 2 * y - Hex.__sqrt3 / 2 * z)

    @staticmethod
    def make_corners(coord: tuple) -> tuple:
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


Hex.make_rings()
