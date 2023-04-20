from math import sqrt

from consts import SCREEN_HEIGHT, SCREEN_WIDTH


class Hex:
    __sqrt3 = sqrt(3)
    __rings = []
    movements = ((1, 0, -1), (0, 1, -1), (1, -1, 0), (-1, 0, 1), (0, -1, 1), (-1, 1, 0))

    # default for map size 11
    radius_x = SCREEN_WIDTH // 40
    radius_y = SCREEN_HEIGHT // 40

    @staticmethod
    def danger_zone(td: tuple, target: tuple) -> tuple:
        # returns the coords of all the hexes that could be affected by a TD shooting from 'td' to 'target'
        target_dir = Hex.dir_vec(td, target)
        danger_zone = [Hex.coord_sum(td, target_dir)]
        for _ in range(2):
            danger_zone.append(Hex.coord_sum(danger_zone[-1], target_dir))
        return tuple(danger_zone)

    @staticmethod
    def td_shooting_coord(td_coord: tuple, target: tuple) -> tuple:
        # Returns the coord where the TD needs to fire to, to hit the tank in 'target' ('target' is in TD fire pattern)
        distance = Hex.manhattan_dist(td_coord, target)
        if distance == 1: return target
        return Hex.coord_sum(target, Hex.coord_mult(Hex.dir_vec(target, td_coord), distance-1))

    @staticmethod
    def possible_shots(tank_coord: tuple, fire_deltas: tuple) -> tuple:
        x, y, z = tank_coord
        return tuple([(dx + x, dy + y, dz + z) for (dx, dy, dz) in fire_deltas])

    @staticmethod
    def opposite_coord(origin: tuple, target: tuple) -> tuple:
        dir_vec = Hex.dir_vec(origin, target)
        rev_dir_vec = Hex.rev_dir_vec(dir_vec)
        return Hex.coord_sum(origin, rev_dir_vec)

    @staticmethod
    def dir_vec(origin: tuple, target: tuple) -> tuple:
        dist = Hex.manhattan_dist(origin, target)
        x1, y1, z1 = origin
        x2, y2, z2 = target
        dx = ((x2-x1)//dist)
        dy = ((y2-y1)//dist)
        dz = ((z2-z1)//dist)
        return dx, dy, dz

    @staticmethod
    def rev_dir_vec(dir_vec: tuple) -> tuple:
        return tuple(-x for x in dir_vec)

    @staticmethod
    def fire_deltas(min_range: int, max_range: int):
        fire_deltas = []
        for i in range(min_range, max_range+1):
            for coord in Hex.__rings[i]:
                fire_deltas.append(coord)
        return tuple(fire_deltas)

    @staticmethod
    def make_rings():
        max_range = 3  # Change if maximum range of any tank is > 3 hexes
        Hex.__rings = [Hex.make_ring(i) for i in range(0, max_range + 1)]

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
    def manhattan_dist(coord1: tuple, coord2: tuple) -> int:
        x1, y1, z1 = coord1
        x2, y2, z2 = coord2
        return (abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)) // 2

    @staticmethod
    def coord_sum(coord1: tuple, coord2: tuple) -> tuple:
        return tuple(fst + snd for fst, snd in zip(coord1, coord2))

    @staticmethod
    def coord_mult(coord: tuple, m: int) -> tuple:
        return tuple(x * m for x in coord)

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
